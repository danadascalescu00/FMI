parent(ion,maria).
parent(ana,maria).
parent(ana,dan).
parent(maria,elena).
parent(maria,radu).
parent(elena,nicu).
parent(radu,george).
parent(radu,dragos).

child(X,Y) :- parent(Y,X).


% Start from the parent relation, define the following relations:
%  - brother(X,Y) (X and Y are brothers)
%  - grandparent(X<Y) (X is grandparent of Y)
brother(X,Y) :- parent(Z,X), parent(Z,Y), X\=Y.
grandparent(X,Y) :- parent(X,Z), parent(Z,Y).


boy(andrei, 21).
boy(alexandru, 20).

ageboys(L) :- findall(Age,boy(_,Age),L).
sum(S) :- ageboys(L), sum(L,S).
sum([],0).
sum([H|T],S) :- sum(T,Aux), S is Aux + H.



% Exercises
% 1) Write the max predicate that calcultaes the maximum between 2
% values.
% Solution 1:
max(X,Y,Ans) :- X=<Y,Ans is Y,!.
max(X,_,Ans) :- Ans is X.

% Solution 2:
maxi(X,Y,Y) :- X<Y,!.
maxi(X,_,X).



% 2) Write the member and concat predicates.
% Solution 1:
memberOf(X,[H|[]]) :- X==H.
memberOf(X,[H|T]) :- X==H; memberOf(X,T).

% Soltion 2:
member2(X,[X|_]).
member2(X,[_,T]) :- member2(X,T).


concatenate([],X,X).
concatenate([H1|T1],L2,[H1|Result]) :- concatenate(T1,L2,Result).



% 3) Calculate the alternate sum of the elements of a list.
alternatesum([],0).
alternatesum([X],X).
alternatesum([A,B|T],S) :- alternatesum(T,Aux), S is A-B+Aux.



% 4) Eliminate an element from a list (one/all occurences of that
% element).

% eliminate first occurence of the element in the list
eliminate(_,[],[]).
eliminate(X,[X|T],T) :- !.
eliminate(X,[Y|T1],[Y|T2]) :- eliminate(X,T1,T2).

% eliminate all occurences of the element in the list
eliminateall(_,[],[]).
eliminateall(X,[X|T],R) :- eliminateall(X,T,R).
eliminateall(X,[Y|T],[Y|R]) :- eliminateall(X,T,R).



% 5) Reverse a list; generate all the permutations of the elements of a
% list.
% Solution 1:
reverseList([],[]).
reverseList([H|T],R) :- reverseList(T,Aux), concatenate(Aux,[H],R).

% Solution 2:
reverse2([],[]).
reverse2([H|T],R) :- reverse2(T,Aux), append(Aux,[H],R).

perm([],[]).
perm([A|B],C) :- perm(B,Aux), insert(A,Aux,C).

insert(A,B,[A|B]).
insert(A,[H|T],[H|R]) :- insert(A,T,R).



% 6) Find the number of occurences of an element in a list.
% Solution 1:
occurences(_,[],0).
occurences(X,[H|T],Result) :- X==H, occurences(X,T,Aux), Result is 1+Aux;
                              occurences(X,T,Aux), Result is Aux.

% Solution 2:
occur(X,L,0) :- not(member(X,L)),!.
occur(X,[X|L],N) :- !,occur(X,L,Aux), N is Aux+1.
occur(X,[_|L],N) :- occur(X,L,N).



% 7) Insert an element on a certain position in a list.
insert(X,1,L,[X|L]).
insert(X,Pos,[H|T],[H|L2]) :- Pos>1, Pos2 is Pos-1, insert(X,Pos2,T,L2).



% 8) Merge two ascending ordered lists.
mergeLists([],L,L) :- !.
mergeLists(L,[],L).
mergeLists([A|B],[C|D],[A|E]) :- A=<E, !, mergeLists(B,[C|D],E).
mergeLists([A|B],[C|D],[C|E]) :- mergeLists([A|B],D,E).

