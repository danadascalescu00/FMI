exercise1 :-
    % open('P1_1d_input4.txt', read, InputFile),
    open('P1_1c_input.txt', read, InputFile),
    read(InputFile,KB), close(InputFile),
    sort(KB,ClausesSorted),
    get_unique_literals(ClausesSorted,UniqueLiterals), eliminate_pure_clauses(ClausesSorted,UniqueLiterals,ResultedClauses),
    eliminate_tautologies(ResultedClauses,ResultedClauses2),
    eliminate_subsumed_clauses(ResultedClauses2,ResultedClauses3),
    resolution(ResultedClauses3).

eliminate_pure_clauses([],_,[]).
eliminate_pure_clauses([H|T],UniqueLiterals,ResultingClauses) :-
    member(Lit,H), negate(Lit,NegatedLit), not(member(NegatedLit,UniqueLiterals)), !, eliminate_pure_clauses(T,UniqueLiterals,Aux), ResultingClauses=Aux;
    eliminate_pure_clauses(T,UniqueLiterals,Aux), ResultingClauses=[H|Aux].

eliminate_tautologies([],[]).
eliminate_tautologies([H|T],ResultingClauses) :-
    member(X,H), member(n(Y),H), X==Y, !, eliminate_tautologies(T,Aux), ResultingClauses=Aux;
    eliminate_tautologies(T,Aux), ResultingClauses=[H|Aux].


eliminate_subsumed_clauses(Clauses,ResultingClauses) :-
    member(Clause1,Clauses), member(Clause2,Clauses), Clause1\==Clause2,
    is_subsumed_clause(Clause1,Clause2), select(Clause2,Clauses,ResultingClauses2),
    eliminate_subsumed_clauses(ResultingClauses2,ResultingClauses);
    ResultingClauses=Clauses.


is_subsumed_clause([],_).
is_subsumed_clause([H|T],Clause2) :-
    contains_literal(H,Clause2), is_subsumed_clause(T,Clause2).


contains_literal(Lit,[Lit|_]).
contains_literal(Lit,[_|T]) :-
    contains_literal(Lit,T).


resolution([]) :-
    write("Satisfiable").
resolution(S) :-
    member([],S) -> write("Unsatisfiable");

    member(Clause1,S), member(Clause2,S), Clause1\==Clause2,
    select(Lit,Clause1,Aux1), select(n(Lit),Clause2,Aux2),
    get_resolvent(Aux1,Aux2,Resolvent),
    append(S,[Resolvent],UnionKB), sort(UnionKB,KB),
    get_unique_literals(KB,UniqueLiterals), eliminate_pure_clauses(KB,UniqueLiterals,ResultedClauses),
    eliminate_tautologies(ResultedClauses,KBFiltered), eliminate_subsumed_clauses(KBFiltered,NewKB),
    not(S=NewKB),
    resolution(NewKB);

    write("Satisfiable").


get_resolvent(Clause1,Clause2,Resolvent) :-
    append(Clause1,Clause2,Reunion), sort(Reunion,Resolvent).



exercise2 :-
    open('P1_2_i_input.txt',read,InputFile), read(InputFile,KB), close(InputFile),
    sort(KB,ClausesCNF),
    (   dp(ClausesCNF,Answer,Output) ->
        write("Satisfiable? "), write(Answer), write("\n"),
        (   Answer="YES" -> write(Output))
    ).


dp([],"YES",[]).
dp(S,"NO",_) :-
    member([],S),!.
dp(S,SAT,Values) :-
    choose_literal_strategy1(S,Literal),
    dot_operation(S,Literal,ResultedClauses),
    dp(ResultedClauses,Ans,Out),
    (   Ans="YES" -> SAT="YES", append([(Literal,"true")],Out,Values),!;

        negate(Literal,NegatedLiteral), dot_operation(S,NegatedLiteral,ResultedClauses2),
        dp(ResultedClauses2,SAT,Out2),
        append([(Literal,"false")],Out2,Values)    ).



choose_literal_strategy1(Clauses,ChosenLiteral) :-
    get_unique_literals(Clauses,UniqueLiterals),
    make_pairs(Clauses,UniqueLiterals,ListPairs),
    sort(0,@>,ListPairs,SortedListPairs),
    second(SortedListPairs,DescendingOrderLiterals),
    get_head_list(DescendingOrderLiterals,ChosenLiteral).


choose_literal_strategy2(Clauses,ChosenLiteral) :-
    get_unique_literals(Clauses,UniqueLiterals),
    make_pairs(Clauses,UniqueLiterals,ListPairs),
    sort(0,@<,ListPairs,SortedListPairs),
    second(SortedListPairs,DescendingOrderLiterals),
    get_head_list(DescendingOrderLiterals,ChosenLiteral).


make_pairs(Clauses,Literals,ListPairs) :-
    maplist(
        {Clauses}/[Lit,Freq]>>get_literal_frequency(Lit,Clauses,Freq),
         Literals,LiteralsCount),
    make_list_pairs(LiteralsCount,Literals,ListPairs).


make_list_pairs([],_,[]).
make_list_pairs(_,[],[]).
make_list_pairs([Head1|Tail1],[Head2|Tail2],[(Head1,Head2)|Rest]) :-
    make_list_pairs(Tail1,Tail2,Rest).


get_unique_literals(Clauses,UniqueLiterals) :-
    flatten(Clauses,LiteralsList), sort(LiteralsList,UniqueLiterals).


get_literal_frequency(Literal,Clauses,Frequency) :-
    get_clauses_containing_literal(Clauses,Literal,SubsetClauses),
    count_clauses(SubsetClauses,Frequency).


get_clauses_containing_literal(Clauses,Literal,ResultingClauses) :-
    include(
        {Literal}/[Clause] >> member(Literal,Clause),
        Clauses,
        ResultingClauses).


count_clauses([],0).
count_clauses([_|T],N):-
    count_clauses(T,Aux), N is Aux+1.


second([],[]).
second([(_,Y)|T],[Y|Rest]) :-
    second(T,Rest).


get_head_list([H|_],H).


dot_operation(SetClauses,Literal,ResultedClauses) :-
    include({Literal}/[Clause]>>not(member(Literal,Clause)),
            SetClauses,
            FilteredClauses),
    negate(Literal,LiteralNegated), include({LiteralNegated}/[Clause]>>not(member(LiteralNegated,Clause)),
                                            FilteredClauses,
                                            SubsetClauses1),
    include({LiteralNegated}/[Clause]>>member(LiteralNegated,Clause),
            SetClauses,
            FilteredClauses2),
    maplist({LiteralNegated}/[Clause,ClauseMinusLit]>>delete(Clause,LiteralNegated,ClauseMinusLit),
            FilteredClauses2,
            SubsetClauses2),
    union(SubsetClauses1,SubsetClauses2,ResultedClauses).


negate(n(X),X) :- !.
negate(X,n(X)).













