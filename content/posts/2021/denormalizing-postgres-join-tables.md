---
type: "post"
aliases:
- /2021/08/denormalizing-postgres-join-tables.html
date: "2021-08-30T00:00:00Z"
tags:
- linux
- fedora
- foreman
title: Denormalizing PostgreSQL join tables
---

Foreman OpenSCAP plugin stores security scanner results in Foreman's PostgreSQL database providing integrated UI, API and CLI experience. To simplify our use case, let's assume that each report has many-to-many association to security rules with some result (pass or fail). This gives us two main SQL tables: report and rule and a join table between them. For simplicity, let's ignore the result which should be an extra column in the join table.

Just for the record, such l report looks like this when presented in UI or CLI:

    Report for host.example.com performed on 2021-01-01 12:30:
    --
    Minimum password length set to 10 characters: PASS
    RPM database is valid: FAIL
    Audit daemon is enabled and running: PASS
    Mount /home has nodev option: PASS
    ...

In typical workflow a report is created, rules associated through join table and it is all kept for some time (from weeks to years depending on user preference) until a cron job deletes old reports. Users search for reports by report date and time, by total number of passing or failed rules, by rule names and rule results. Now, the current design using normal form with the join table is extremely slow when amount of records in the join table goes into higher counts, almost all operations are slow - inserting, selecting, and, believe it or not, deleting is huge pain. When database is under heavy load and more and more new reports are being inserted, postgres needs to lock the table when deleting records and since the deletion process is also slow, users experience transaction errors.

There must be more efficient way of storing reports, perhaps avoiding the join table alltogether. The use case is heavy on data insert and delete (thousands of hosts can upload their reports per hour) while searching is not performed very often (few dozens of searches per day typically). My very first idea was to store rules in a text column and searching could be performed as a regular expression table scan. I implemented the first prototype, but then I stumbled upon array data type and GIN index with intarray extension.

It is simple, report ids can be stored in a multiple array columns: passing_rules and failed_rules. When presenting report to screen, rules can be easily retrieved and sorted by name or result. Inserts and deletes will be much faster as there is no join table and data should be stored pretty efficiently. But searching is big question I need to test - table scan is probably not an option, however, there is a way to create index on array column.

Let's simulate the old scenario with the join table by creating the following tables:

* `rule` - rule name and id
* `report_association` - report name and id
* `report_association_rule` - join table between report_association and rule

Typical report has somewhere between 50 and 100 rules and typical Foreman deployment has tens of thousands of hosts with tens of reports kept in the database, until they are deleted. I performed testing with 100000 records and 500 rules associated for each record from pool of 5000 rules total.

    # select count(*) from rule;
     count
    -------
      5000
    (1 row)

    # select count(*) from report_association;
     count
    --------
     100000
    (1 row)

    # select count(*) from report_association_rule;
      count
    ----------
     50000000
    (1 row)

This gives us a good starting point - 50 million records in join table. I know there are users with more records, but this should give us rough idea and keep testing reasonably fast on my hardware. Now, let's create a second table which will hold reports and rules in an array column:

* `report_array` - report name, id and int arrays rules_fail, rules_pass

Let's create a new database and do some DDL statements:

    create table rule (id serial primary key, name varchar not null);
    create table report_association (id serial primary key, name varchar not null);

    create table report_association_rule (
      report_id int references report_association(id) on update cascade on delete cascade,
      rule_id int references rule(id) on update cascade on delete cascade
    );

    create table report_array (id serial primary key, name varchar not null, rules_fail int[], rules_pass int[]);

Time to load some data. For names let's use MD5 hexstring of primary key just to have something to show. Create rules and reports:

    insert into rule(name) select md5(generate_series::text) from generate_series(1, 5000);
    insert into report_association(name) select md5(generate_series::text) from generate_series(1, 100000);

Now, let's create associations for the join table and at the same time, insert records into the table which stores associations in arrays. This will ensure both queries are giving exactly same results. The following block will pick 500 rules (or less as duplicite values are eliminated) from the rule table randomly and then insert records into the join table and then into the report_array table as well:

    do $$
    declare
      rules int[];
      report_id int;
      rule_id int;
    begin
      for report_id in 1..100000 loop
        rules := array_agg(distinct round(random() * (5000 - 1)) + 1) from generate_series (1, 500);
        -- association
        foreach rule_id in array rules loop
          insert into report_association_rule(report_id, rule_id) values (report_id, rule_id);
        end loop;
        -- array column
        insert into report_array(name, rules_fail, rules_pass) values (md5(report_id::text), rules, rules);
      end loop;
    end; $$;

Creating records in a loop ensures that associations are the same for both join table and array columns. Before we create any indices, let's try table scan across all reports finding rule with id 747. I executed every query several times so data could be loaded into memory and cache and picked a typical (read "average") result. First off, via join table:


    explain analyze select report_association.name from report_association inner join report_association_rule on report_association.id = report_association_rule.report_id where report_association_rule.rule_id = 747;
                                                                             QUERY PLAN
    ------------------------------------------------------------------------------------------------------------------------------------------------------------
     Gather  (cost=1000.29..463425.99 rows=9484 width=33) (actual time=0.305..1609.657 rows=9510 loops=1)
       Workers Planned: 2
       Workers Launched: 2
       ->  Nested Loop  (cost=0.29..461477.59 rows=3952 width=33) (actual time=0.205..1597.797 rows=3170 loops=3)
             ->  Parallel Seq Scan on report_association_rule  (cost=0.00..458402.31 rows=3952 width=4) (actual time=0.176..1580.169 rows=3170 loops=3)
                   Filter: (rule_id = 747)
                   Rows Removed by Filter: 15858843
             ->  Index Scan using report_association_pkey on report_association  (cost=0.29..0.78 rows=1 width=37) (actual time=0.004..0.004 rows=1 loops=9510)
                   Index Cond: (id = report_association_rule.report_id)
     Planning Time: 0.193 ms
     Execution Time: 1610.327 ms

Now via array column:

    explain analyze select report_array.name from report_array where report_array.rules_fail @> '{747}';
                                                        QUERY PLAN
    ------------------------------------------------------------------------------------------------------------------
     Seq Scan on report_array  (cost=0.00..24725.00 rows=500 width=33) (actual time=0.045..865.309 rows=9510 loops=1)
       Filter: (rules_fail @> '{747}'::integer[])
       Rows Removed by Filter: 90490
     Planning Time: 0.094 ms
     Execution Time: 866.616 ms

Array is already two times faster via table scan. Both queries returned 9510 results, to confirm they are processing the same data. Let's create indices, first the join table:

    create index ix_report_association_rule_report_id on report_association_rule(report_id);
    create index ix_report_association_rule_rule_id on report_association_rule(rule_id);

Now, let's create index for array to speed up searching by rule id. There are couple of options in PostgreSQL 12:

* GIN with default operators
* GIN with operators from intarray extension
* GiST with operators for small arrays from intarray extension
* GiST with operators for large arrays from intarray extension

The intarray extension provides functions, operators and optimized index for integer (int4 only) arrays. However, I was not able to see any difference for this use case. I asked on PostgreSQL IRC channel and guys told me that intarray could show its potential for very large datasets (larger arrays than hundreds of elements) or more complex queries.

I tried both GIN and GiST types and GiST index was smaller, faster for updates but slower for search. Since GIN index type is recommended for arrays and GIN without intarray extension was giving me exactly the same results, I have decided to use just plain GIN index type. Feel free to test intarray extension and compare results to plain GIN index and let me know if you are able to see any difference. In that case, load the extension and create indices using opclasses:

    -- DO NOT do this unless you want to compare intarray performance
    create extension intarray;
    create index ix_report_array_rules_pass on report_array using gist(rules_pass gist__intbig_ops);
    create index ix_report_array_rules_fail on report_array using gin(rules_fail gin__int_ops);

So let's create GIN indices on both passed and failed rules. No extension is required, this is also possible to do in Ruby on Rails without writing any SQL statements:

    create index ix_report_array_rules_pass on report_array using gin(rules_pass);
    create index ix_report_array_rules_fail on report_array using gin(rules_fail);

Before we do any select statements, let's take a moment and see how much data is used. First, just data:

    select pg_size_pretty(pg_table_size('report_association') + pg_table_size('report_association_rule'));
     pg_size_pretty
    ----------------
     1652 MB

    select pg_size_pretty(pg_table_size('report_array'));
     pg_size_pretty
    ----------------
     395 MB

It is no surprise that data stored in arrays are more compact, after all it is just a single table versus two tables. Let's count size of indexes:


    select pg_size_pretty(pg_indexes_size('report_association') + pg_indexes_size('report_association_rule'));
     pg_size_pretty
    ----------------
     2044 MB

    select pg_size_pretty(pg_indexes_size('report_array'));
     pg_size_pretty
    ----------------
     345 MB

It looks like GIN indexes on arrays are significantly smaller than index on join table. Just for the record, here are total numbers:

    select pg_size_pretty(pg_total_relation_size('report_association') + pg_total_relation_size('report_association_rule'));
     pg_size_pretty
    ----------------
     3696 MB

    select pg_size_pretty(pg_total_relation_size('report_array'));
     pg_size_pretty
    ----------------
     740 MB

Good, so what we know until now is that array of integers is faster on table scan and both data and indexes are more compact. But more important question to answer is searching with index. Will GIN index outperform B-Tree on a join table? Let's find out, analysis of the traditional approach via join table:

    explain analyze select report_association.name from report_association inner join report_association_rule on report_association.id = report_association_rule.report_id where report_association_rule.rule_id = 747;
                                                                           QUERY PLAN
    ---------------------------------------------------------------------------------------------------------------------------------------------------------
     Hash Join  (cost=4048.07..36312.66 rows=9484 width=33) (actual time=38.989..60.094 rows=9510 loops=1)
       Hash Cond: (report_association_rule.report_id = report_association.id)
       ->  Bitmap Heap Scan on report_association_rule  (cost=182.07..31563.76 rows=9484 width=4) (actual time=2.658..12.127 rows=9510 loops=1)
             Recheck Cond: (rule_id = 747)
             Heap Blocks: exact=9510
             ->  Bitmap Index Scan on ix_report_association_rule_rule_id  (cost=0.00..179.69 rows=9484 width=0) (actual time=1.401..1.401 rows=9510 loops=1)
                   Index Cond: (rule_id = 747)
       ->  Hash  (cost=1834.00..1834.00 rows=100000 width=37) (actual time=36.153..36.154 rows=100000 loops=1)
             Buckets: 65536  Batches: 4  Memory Usage: 2272kB
             ->  Seq Scan on report_association  (cost=0.00..1834.00 rows=100000 width=37) (actual time=0.010..16.153 rows=100000 loops=1)
     Planning Time: 0.222 ms
     Execution Time: 60.400 ms

Only 60ms, that is a very good result, now arrays with index:

    explain analyze select report_array.name from report_array where report_array.rules_fail @> '{747}';
                                                                   QUERY PLAN
    -----------------------------------------------------------------------------------------------------------------------------------------
     Bitmap Heap Scan on report_array  (cost=19.88..1790.49 rows=500 width=33) (actual time=2.705..8.456 rows=9510 loops=1)
       Recheck Cond: (rules_fail @> '{747}'::integer[])
       Heap Blocks: exact=8170
       ->  Bitmap Index Scan on ix_report_array_rules_fail  (cost=0.00..19.75 rows=500 width=0) (actual time=1.625..1.625 rows=9510 loops=1)
             Index Cond: (rules_fail @> '{747}'::integer[])
     Planning Time: 0.067 ms
     Execution Time: 8.729 ms

Only 9ms, that is significantly faster. We almost have a winner, now the most important part: performance of updates (insert). In our use case, the bottleneck is performance of report uploads which tend to slow down once indexes cannot fit into memory. Let's measure 1000 inserts into the join table, then the same amount of inserts into report table with arrays:

    \timing on
    do $$
    declare
      rules int[];
      report_id int;
      rule_id int;
    begin
      for report_id in 1..1000 loop
        rules := array_agg(round(random() * (5000 - 1)) + 1) from generate_series (1, 500);
        foreach rule_id in array rules loop
          insert into report_association_rule(report_id, rule_id) values (report_id, rule_id);
        end loop;
      end loop;
    end; $$;
    Time: 26055,616 ms (00:26,056)

    do $$
    declare
      rules int[];
      report_id int;
      rule_id int;
    begin
      for report_id in 1..1000 loop
        rules := array_agg(round(random() * (5000 - 1)) + 1) from generate_series (1, 500);
        insert into report_array(name, rules_fail, rules_pass) values (md5(report_id::text), rules, rules);
      end loop;
    end; $$;
    Time: 2456,793 ms (00:02,457)
    \timing off

Inserting 1000*500 records into join table with 50 million of records takes 26 seconds, inserting 1000 records with two arrays with 500 elements into table with 100000 records takes 2.5 seconds. This includes updating of indexes, that is great performance.

In conclusion, it is possible to save significant amount of disk, memory and cpu cycles by denormalizing join tables with integer array column containing primary keys or associated table. It makes sense in scenarios with heavy updates, searching with or without index is also faster. On the other hand, records must be fetched manually and there is no database integrity. This is fine for this specific case (reports kept for record purposes). Also this test was performed with small number of associated records (up to 1:500), your mileage may vary.

