% 1) Compute the greatest common divisor of two integers - gcd/3;
gcd(X,0,X):-!.
gcd(0,X,X):-!.
gcd(A,B,C):-A=<B,D is B-A, gcd(D,B,C).
gcd(A,B,C):-D is A-B, gcd(D,B,C).



% 2) Split a list into 2 lists, according to a given value: the elements
% that are less than the value are placed in the first list and the
% elemnts greater or equal than thr value are placed in the second list
% - split/4
split([],_,[],[]).
split([H1|T],H,[H1|A],B):-H1=<H,!, split(T,H,A,B).
split([H1|T],H,A,[H1|B]):- split(T,H,A,B).



% 3) Insertion sort and quick sort - insertsor/2 and quicksort/2;
insertSort([],[]).
insertSort([X|T],S):-insertSort(T,S2), insertOrder(X,S2,S).

% insertOrder(Elem,OrderedList,OrderedListNew) -- insert the element
% Elem on its right position in OrderedList and the result is
% OrderedListNew
insertOrder(X,[],[X]).
insertOrder(X,[Y|T],[X,Y|T]):-X=<Y,!.
insertOrder(X,[Y|T],[Y|T2]):-insertOrder(X,T,T2).


quickSort([],[]).
quickSort([X],[X]).
quickSort([H|T],L):-split(T,H,A,B),quickSort(A,A1),quickSort(B,B1),concat(A1,[H],C),concat(C,B1,L).


% Other exercises for practice:
% Duplicate all the elements of a list.
duplicateElements([],[]).
duplicateElements([X|T],[X,X|L]):-duplicateElements(T,L).

% Find the position of an element in a list.
findPos(_,[],-1).
findPos(X,L,-1):-not(member(X,L)),!.
findPos(X,[X|_],Pos):-Pos is 1,!.
findPos(X,[_|T],Pos):-findPos(X,T,Pos2),!,Pos is Pos2+1.

