
%% uvazujme uplny neorientovany hranove ohodnoceny graf G
%% kde uzly ocislujme 1...5

%% s temito hranami (posledni cislo representuje ohodnoceni)
edge(a,b,7).
edge(b,c,2).
edge(c,d,4).
edge(d,e,8).
edge(e,a,3).
edge(a,c,9).
edge(a,d,6).
edge(b,e,4).
edge(b,d,1).
edge(c,e,5).

%% a nyni to nejdulezitejsi; co to umi:
%% a) vyhledat vsechny mozne cesty mezi dvema uzly se souctem jejich ohodnoceni
%%    Pr. path(2,4,C).
%% b) vyhledat cestu mezi dvema uzly (nejkratsi)
%%    Pr. mpath(1,5,C). 

%% hrany nejsou orientovane (usnadneni prace)
connected(X,Y,H) :- edge(X,Y,H).
connected(X,Y,H) :- edge(Y,X,H).

%% predikat generujici vsechny mozne cesty mezi dvema uzly
%% zacni s prochazinem u uzlu A a vysledek prevrat
path(A,B,[Path|Val]) :- travel(A,B,[A],Q,Val), reverse(Q,Path).

%% vlastni implementace prochazeni
%% limitni podminka "rekurze", pokud je uzel primo spojen
travel(A,B,P,[B|P],Val) :- connected(A,B,Val).
%% najdi dalsi cestu pricemz
travel(A,B,Visited,Path,ValR) :- connected(A,C, Val), % A musi byt spojen s C
	C \== B, % C neni B
	not(member(C,Visited)), % C jeste nebyl navstiven
	travel(C,B,[C|Visited],Path, Val2), % najdi takove C
	ValR is (Val + Val2). % a secti ohodnoceni jako cisla

%% vybere z cest tu s nejmensim ohodnocenim
%% Pr.: mpath(a,c,X).
mpath(A,B,Minimal) :- setof(Set,path(A,B,Set),Set), selmin(Set,Minimal).

%% jako horni hranici stanovme napr. milion
selmin(Set,Minimal) :- select_minimal(Set, 1000000, _, Minimal).
select_minimal([],_,Result,Result).
select_minimal([[M|V]|Nxt],ActV,ActS,Res) :-
	(V @< ActV -> MinV = V, MinS = M ; MinV = ActV, MinS = ActS), select_minimal(Nxt,MinV,MinS,Res).

%% vybere vsechny sousedy uzlu, ktere jsou v seznamu (resp. v kruznici)
incid(U,S,[V|H]) :- connected(U, V, H), member(V, S).

%% vrati vzdalenost uzlu od kruznice
%% Pr.: distance(a, [b,c,d], X).
distance(U,K,V) :- setof(Set,incid(U,K,Set),Set), mincid(Set,V).
mincid(Set,Minimal) :- mincid(Set, 1000000, Minimal).
mincid([],Result,Result).
mincid([[_|V]|Nxt],ActV,Res) :- (V @< ActV -> MinV = V ; MinV = ActV), mincid(Nxt,MinV,Res).

%% vrati uzel s nejvetsi vzdalenosti od kruznice
%% pokud je takovych uzlu vice, vraci prvni z nich
%% Pr.: mdist([a,e], [b,c,d], X).
mdist(N,C,R) :- mdist(N,C,[],S), selmax(S,MaxV), setof(Y,member([Y|MaxV],S),Y), nth1(1,Y,R).
% mdist/4 vrati seznam uzlu a jejich vzdalenosti
mdist([],_,R,R).
mdist([N|Nodes],Circle,Act,Res) :- distance(N,Circle,D), mdist(Nodes,Circle,[[N|D]|Act],Res).
% selmax vybere nejvetsi vzdalenost, ktera se pote dohleda pomoci setof a member
selmax(Set,Max) :- selmax(Set,0,Max).
selmax([],Result,Result).
selmax([[_|V]|Nxt],ActV,Res) :- (V @> ActV -> MaxV = V ; MaxV = ActV), selmax(Nxt,MaxV,Res).

%% vrati seznam bez vsech prvku Y
%% Pr.: remove(Y,[x,y,z],R). => [x,z]
remove(P,S,V) :- reverse(S,SR), remove(P,SR,[],V).
remove(_,[],V,V).
remove(P,[H|T],M,V) :- (H == P -> remove(P,T,M,V) ; remove(P,T,[H|M],V)).

%% vrati ohodnoceni uzavrene cesty
%% Pr.: eval([b,c,d],E).
eval([U1|S],E) :- last(U2,S), connected(U1,U2,I), eval([U1|S],I,E).
eval(.(_,[]),R,R).
eval([A,B|S],E,Result) :- connected(A,B,V), NewVal is (E+V), eval([B|S],NewVal,Result).

%% zatridi uzel tak, aby ohodnoceni cesty bylo nejmensi
%% Pr.: insert(e, [b,c,d], X).
insert(U,S,R) :- options(U,S,ALL), getminpath(ALL,R).
% generuje vsechny moznosti vlozeni, kterych je vzdy n (vraci jako seznam)
% Pr.: options(x, [a,b,c], R).
options(X,S,V) :- options(X,[],S,[],V).
options(_,_,[],X,X).
options(U,Z,[F|S],A,R) :- reverse(Z,ZR), append(ZR,[U,F|S],ZF), options(U,[F|Z],S,[ZF|A],R).
% vybere z cest tu s nejmensim ohodnocenim
getminpath(S,R) :- getminpath(S,1000000,_,R).
getminpath([],_,Result,Result).
getminpath([Path|Nxt],ActV,ActP,Res) :-
		eval(Path,V),
		(V @< ActV -> MinV = V, MinP = Path ; MinV = ActV, MinP = ActP),
		getminpath(Nxt,MinV,MinP,Res).

%% ULOHA OBCHODNIHO CESTUJICIHO
solve(Kruznice,ZbUzly,Vysledek) :-
	%% vrat nejvzdalenejsi uzel (U)
	mdist(ZbUzly,Kruznice,U),
	%% vloz ho tak, aby bylo oh. kruznice nejmensi
	insert(U,Kruznice,NovaKruznice),
	%% tento uzel vyjmi ze seznamu zbylych uzlu
	remove(U,ZbUzly,NoveZbUzly),
	%% a rekurzivne pokracuj pro dalsi uzel
	solve(NovaKruznice,NoveZbUzly,Vysledek).

%% limitni podminka rekurze
solve(Kruznice,[],Kruznice).

%% vim:tw=100
