import Data.Char (isDigit, digitToInt, isAlpha)

f :: [Char] -> [Char]
f "" = ""
f (x:y:xs) 
    | y `elem` ['.', ',', ';', ':', '!', '?', ')'] && x == ' ' = [y] ++ f xs 
    | x `elem` ['.', ',', ';', ':', '!', '?', ')'] && y /= ' ' = [x] ++ " " ++ [y] ++ f xs
    | x == ' ' && y == '(' = [x] ++ [y] ++ f xs
    | x /= ' ' && y == '(' = [x] ++ " " ++ [y] ++ f xs
    | x == '(' && y == ' ' = [x] ++ f xs
    | otherwise =  [x] ++ [y] ++ f xs



-- O functie care pentru un sir de caractere calculeaza suma codificarilor caracterelor din sir folosind urmatoarea codificare:
-- Caracterul e vocala => 1
-- Caracterul e consoana => 2
-- Caracterul e cifra => 3
-- Orice altceva => -1
codificareSir :: [Char] -> Int
codificareSir [] = 0
codificareSir (x:xs)
    | x `elem` "aeiouAEIOU" = 1 + codificareSir xs
    | isAlpha x = 2 + codificareSir xs
    | isDigit x = 3 + codificareSir xs
    | otherwise = -1 + codificareSir xs


-- Sa se scrie o functie care pentru doua liste, x si y, calculeaza suma produselor 
-- xi^2 * yi^2 cu xi din x si yi din y. Daca listele au lungimi diferite, functia va arunca o eroare.
--  f [1,2,3,4] [5,6,7,8] == (1^2 * 5^2)  + (2^2*6^2) + (3^2*7^2)
-- Rezolvati aceasta problema folosind functii de nivel inalt (fara recursie si descrieri de liste, fara functia sum)
funAux :: Num b => [b] -> [b] -> b
funAux l1 l2 =   foldr ((+) . (\ (x, y) -> x * x * y * y)) 0 (zip l1 l2)

fun :: Num p => [p] -> [p] -> p
fun l1 l2 
    | length l1 == length l2 = funAux l1 l2
    | otherwise = error "The lists don't have the same length"


-- Sa se scrie o functie care pentru o lista de numere intregi l si 2 numere x si y afiseaza lista 
-- formata din listele de divizori ale pozitiilor elementelor din intervalul [x,y]. Pozitiile incep de la 0.
-- f [1,5,2,3,8,5,6] 2 5 = [[1],[1,2],[1,3],[1,5]]
-- Puteti folosi doar descrieri de liste (list comprehension) si functii din categoriile A si B
factori :: Integral a => a -> [a]
factori n = [ x | x <- [1..n], n `mod` x == 0 ]

func :: [Integer] -> Integer -> Integer -> [[Integer]]
func l x y = [ factori poz | (el,poz) <- zip l [0..], el>=x && el<=y ]


-- Funcție care elimină literele duplicate consecutive dintr-un șir.
-- Doar recursie și funcții din categoria A.
eliminateDuplicatesRec :: Eq a => [a] -> [a]
eliminateDuplicatesRec [] = []
eliminateDuplicatesRec [elem] = [elem]
eliminateDuplicatesRec (x:y:rest)
    | x == y =  eliminateDuplicatesRec rest
    | otherwise = x : y : eliminateDuplicatesRec rest


eliminateDuplicatesRec' :: Eq a => [a] -> [a]
eliminateDuplicatesRec' [] = []
eliminateDuplicatesRec' [x] = [x]
eliminateDuplicatesRec' (x:y:xs) 
    | x == y = eliminateDuplicatesRec' (x:xs)
    | otherwise = x : y : eliminateDuplicatesRec xs


-- Tipuri de date din enunț
data Pereche = P Int Int
    deriving (Show)

newtype Lista = L [Pereche]
    deriving (Show)

data Exp = I Int | Add Exp Exp | Mul Exp Exp

instance Show Exp where
    show (I a) = show a
    show (Add a b) = "( " ++ show a ++ " + " ++ show b ++ " )"
    show (Mul a b) = "( " ++ show a ++ " * " ++ show b ++ " )"

class ClassExp m where
    toExp :: m -> Exp


instance ClassExp Lista where
    -- Converteste lista de perechi intr-o suma,
    -- in care numerele din fiecare pereche sunt inmultite intre ele.
    toExp (L lista) = toExpAux lista
        where
            prelucreazaPereche (P a b) = Mul (I a) (I b)
            toExpAux [] = I 0
            toExpAux [x] = prelucreazaPereche x
            toExpAux (x:xs) = Add (prelucreazaPereche x) (toExpAux xs)