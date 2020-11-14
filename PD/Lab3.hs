import  Data.List

factori :: Int -> [Int]
factori x = [ n | n <- [1..x], x `mod` n == 0 ]

prim :: Int -> Bool
prim x = factori x == [1,x]

numerePrime :: Int -> [Int]
numerePrime n = [num | num <- [2..n], prim num]

myzip3 :: [Int] -> [Int] -> [Int] -> [(Int, Int, Int)]
myzip3 _ _ [] = []
myzip3 _ [] _ = []
myzip3 [] _ _ = []
myzip3 (x:xs) (y:ys) (z:zs) = (x,y,z) : myzip3 xs ys zs

myZip3 l1 l2 l3 = zipAux (zip l1 l2) l3
    where 
        zipAux _ [] = []
        zipAux [] _ = []
        zipAux ((x,y):xys) (z:zs) = (x,y,z) : zipAux xys zs


--------------------------------------------------------
----------FUNCTII DE NIVEL INALT -----------------------
--------------------------------------------------------
aplica2 :: (a -> a) -> a -> a
aplica2 f x = f (f x)
--aplica2 f = f.f
--aplica2 f = \x -> f (f x)
--aplica2  = \f x -> f (f x)

-- firstElem l = map(\ (x, y) -> x) l
firstElem :: [(b1, b2)] -> [b1]
firstElem = map fst 

sumList :: [[Int]] -> [Int]
sumList = map sum

prel2 :: [Integer] -> [Integer]
prel2 = map (\x -> if even x then x `div` 2 else x*2)

filtrareSir :: (Foldable t, Eq a) => a -> [t a] -> [t a]
filtrareSir ch = filter (elem ch)

patrateImpare :: [Integer] -> [Integer]
patrateImpare = map (^2) . filter odd

patratePozitiiImpare :: [Integer] -> [Integer]
patratePozitiiImpare = map ( (^2) . snd) . filter (odd . fst) . zip [0..]

eliminaConsoane :: [[Char]] -> [[Char]]
eliminaConsoane = map (filter (`elem` "aeiouAEIOU"))

mymap :: (t -> a) -> [t] -> [a]
mymap _ [] = []
mymap f (x:xs) = f x : mymap f xs

myfilter :: (a -> Bool) -> [a] -> [a]
myfilter _ [] = []
myfilter p (x:xs)
    | p x = x : myfilter p xs
    | otherwise = myfilter p xs


sieveEratosthenes n = sieveRec [2..n]
    where
        sieveRec [] = []
        sieveRec (x:xs) = x : sieveRec (filter(\n -> n `rem` x /= 0) xs)

numerePrimeCiur n = sieve [2..n]
          where
          sieve [] = []
          sieve (p:xs) = p : sieve [x | x <- xs, rem x p > 0]


ordonataNat [ ] = True
ordonataNat [ _ ] = True
ordonataNat ( x : xs ) =
    let 
        y = head xs 
    in x < y && ordonataNat xs


ordonataNat1 [ ] = True
ordonataNat1 [ _ ] = True
ordonataNat1 l = and [x < y| (x,y) <- zip l (tail l)]


ordonata :: [a] -> (a -> a -> Bool) -> Bool
ordonata [] _ = True
ordonata l p = and [p x y | (x,y) <- zip l (tail l)]

(*<*) :: ( Integer , Integer ) -> ( Integer , Integer ) -> Bool
(*<*) (a,b) (c,d) = a<c && b<d

compuneList :: (b -> c) -> [(a -> b)] -> [(a -> c)]
compuneList f lf =  map ( f . ) lf

aplicaList a lf = map(\f -> f a) lf


myzip3' a b c = map (\(x,(y, z)) -> (x, y, z))  (zip a (zip b c))