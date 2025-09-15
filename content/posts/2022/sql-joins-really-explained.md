---
type: "post"
aliases:
- /2022/09/sql-joins-really-explained.html
date: "2022-09-02T00:00:00Z"
tags:
- linux
- fedora
- really
title: SQL joins really explained
---

I've got asked how SQL joins *really* work. Let me explain *real quick*,
imagine a database of student with a simple (1:N) relationship, a city students
are from. I will use the tiny SQLite3 database system, you can do this too:

	$ sqlite3 joins.sqlite3
	SQLite version 3.36.0 2021-06-18 18:36:39
	Enter ".help" for usage hints.

Create tables city and student:

	sqlite> create table city (id integer, name text);
	sqlite> create table student (id integer, name text, city_id integer);

Insert few rows:

	sqlite> insert into city (id, name) values (1, 'Prague'), (2, 'New York');
	sqlite> insert into student (id, name, city_id) values (1, 'John', 1), (2, 'Eve', 1), (3, 'Mary', 2);

We have three students from two cities in total, each student having an id of
city they are from:

	sqlite> select * from city;
	1|Prague
	2|New York

	sqlite> select * from student;
	1|John|1
	2|Eve|1
	3|Mary|2

Now, it's possible to select rows from more than one table, in that case
database systems return what is technically called *cartesian product* which is
nothing else than "all options possible". Because select statement always
returns one table, it has to do it that way. Number of rows is the total number
of rows from one table multiplied by number from the other table: `2*3=6`:

	sqlite> select * from student, city;
	1|John|1|1|Prague
	1|John|1|2|New York
	2|Eve|1|1|Prague
	2|Eve|1|2|New York
	3|Mary|2|1|Prague
	3|Mary|2|2|New York

The order of tables in the select statement does not matter, it's the same
result with different column order:

	sqlite> select * from city, student;
	1|Prague|1|John|1
	1|Prague|2|Eve|1
	1|Prague|3|Mary|2
	2|New York|1|John|1
	2|New York|2|Eve|1
	2|New York|3|Mary|2

It is possible to use where clause the same way as in other statements, to
limit the result. Let's filter out only those rows where city `id` equals
student's `city_id` column:

	sqlite> select * from student, city where city.id = student.city_id;
	1|John|1|1|Prague
	2|Eve|1|1|Prague
	3|Mary|2|2|New York

This is typically what we want! Because equality is *commutative*, technically
speaking, you can swap the columns in the where clause only to get the very
same result:

	sqlite> select * from student, city where student.city_id = city.id;
	1|John|1|1|Prague
	2|Eve|1|1|Prague
	3|Mary|2|2|New York

Now here is a thing, *inner join* is exactly that, but with different syntax:

	sqlite> select * from student inner join city on city.id = student.city_id;
	1|John|1|1|Prague
	2|Eve|1|1|Prague
	3|Mary|2|2|New York

Swapping columns in the where clause does not change the result either:

	sqlite> select * from student inner join city on student.city_id = city.id;
	1|John|1|1|Prague
	2|Eve|1|1|Prague
	3|Mary|2|2|New York

The same goes for from/join clauses, it really does not matter which table goes
first in the from or join statements, the only thing that changes is column
order, results are exactly the same:

	sqlite> select * from city inner join student on student.city_id = city.id;
	1|Prague|1|John|1
	1|Prague|2|Eve|1
	2|New York|3|Mary|2

	sqlite> select * from student inner join city on student.city_id = city.id;
	1|John|1|1|Prague
	2|Eve|1|1|Prague
	3|Mary|2|2|New York

To recap, the following are all *inner join* statements giving you the same
results:

	sqlite> select * from student, city where city.id = student.city_id;
	sqlite> select * from student, city where student.city_id = city.id;
	sqlite> select * from student inner join city on city.id = student.city_id;
	sqlite> select * from student inner join city on student.city_id = city.id;
	sqlite> select * from city inner join student on student.city_id = city.id;
	sqlite> select * from student inner join city on student.city_id = city.id;

Which one to choose from when you want to do an inner join? It's up to you, all
relational database systems I know will work the same. The final touch is to
select only the columns you want. Here is our list of students and their home
cities:

	sqlite> select student.name,city.name from student, city where city.id = student.city_id;
	John|Prague
	Eve|Prague
	Mary|New York

But how about *left join* and *right join*? Well, they only matter if you have
null values in the database, which is not this case:

	sqlite> select * from student inner join city on city.id = student.city_id;
	1|John|1|1|Prague
	2|Eve|1|1|Prague
	3|Mary|2|2|New York
	
	sqlite> select * from student left join city on city.id = student.city_id;
	1|John|1|1|Prague
	2|Eve|1|1|Prague
	3|Mary|2|2|New York

Let's set city for the student with id of 2 to null:

	sqlite> update student set city_id = null where id = 2;

	sqlite> select * from student;
	1|John|1
	2|Eve|
	3|Mary|2

Let's do the inner join using one of the syntaxes I explained above and notice
the student is no longer there because Eve has null value for their `city_id`:

	sqlite> select * from student, city where city.id = student.city_id;
	1|John|1|1|Prague
	3|Mary|2|2|New York

The thing is, null equals to nothing, therefore a student with null city id
will never match. The solution? *Left join* will make the system to join rows
from the left table (the word after `from`) even if there are no matches from
the right table (the word after `join`):

	sqlite> select * from student left join city on city.id = student.city_id;
	1|John|1|1|Prague
	2|Eve|||
	3|Mary|2|2|New York

See, student number 2 is now included (compare with the inner join above).
Since they have `city_id` set to null, they would have been filtered out. Very
often, that's probably not what we want to do. When you swap tables in the
statement, it does not work:

	sqlite> select * from city left join student on city.id = student.city_id;
	1|Prague|1|John|1
	2|New York|3|Mary|2

This is where the right join comes, it will do the same thing, but from other
side. Unfortunately, SQLite does not support right joins. Why? Because you
don't need both, you can always do it one way. Most database systems, however,
supports both directions. It's just most of programmers tend to stick just with
one direction for life, I am a left-joiner as well as SQLite3 author I guess.

Instead of looking at diagrams with two potatoes, remember this: *inner join* filters from *product* of both tables leaving out rows with null values, *left join* leaves rows with null values from the *left* table and *right join* does exactly the same, but from the *right* side.

There are also special joins: *outer join* and *full join* but I am not going
to explain them in this article as they are less useful in practice.

Bonus takeaway: If you don't have any null values in your join columns (typically
named `id` for primary keys or `something_id` of `id_something` for foreign
keys), you can just use *inner join* and you are good.

Cheers!

