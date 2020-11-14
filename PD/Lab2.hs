import Data.Char (isDigit, digitToInt)

-------------------------------------------------------------------------------
------------------------------RECURSIE: FIBONACCI------------------------------
-------------------------------------------------------------------------------
fibonacciCazuri :: Integer -> Integer
fibonacciCazuri n 
    | n < 2 = n
    | otherwise = fibonacciCazuri(n-2) + fibonacciCazuri(n-1)


fibonacciEcuational 0 = 0
fibonacciEcuational 1 = 1
fibonacciEcuational n = fibonacciEcuational(n-2) + fibonacciEcuational(n-1)


fibonacciLiniar 0 = 1
fibonacciLiniar n = snd (fibonacciPereche n)
    where
        fibonacciPereche 1 = (0,1)
        fibonacciPereche n = (b,a+b)
            where (a,b) = fibonacciPereche(n-1)
            
-- let (a,b) = fibonacciPereche(n-1) in (b,b+a)


-- Exemplu 2 - Data fiind o lista de intregi, sa se scrie o functie semiPare care elimina din lista numere impare
-- si le injumatateste pe cele pare
semiPare :: [Int] -> [Int]
semiPare l
    | null l = l
    | even h = h `div` 2 : t'
    | otherwise = t'
    where
        h = head l
        t = tail l
        t' = semiPare t


semiPareRecEq :: [Int] -> [Int]
semiPareRecEq [] = []
semiPareRecEq (h:t)
    | even h = h `div` 2 : t'
    | otherwise = t'
    where t' = semiPareRecEq t


semiPareComp :: [Int] -> [Int]
semiPareComp l = [x `div` 2| x <- l, even x]


---------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------Exercitii--------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------
--1. Scrieti o functie in care date fiind limita inferioara si limita superioara(intregi) a unui interval inchis
-- si o lista de numere intrgi, returneaza lista numerelor din lista care apartin intervalului

-- Varianta 1 - folosind recursie
inIntervalRec :: Int -> Int -> [Int] -> [Int]
inIntervalRec _ _ [] = []
inIntervalRec a b (h:t)
    | h >= a && h <= b = h : (inIntervalRec a b t)
    | otherwise = (inIntervalRec a b t)

-- Varianta 2 - folosind descrieri de liste
inIntervalComp :: Int -> Int -> [Int] -> [Int]
inIntervalComp a b l = [x | x <- l, a <= x && x <= b]


--2. Scrieti o functie care numara cate numere strict pozitive sunt intr-o lista data ca argument. 
pozitiveRec :: [Integer] -> Integer
pozitiveRec [] = 0
pozitiveRec (x:xs)
    | x > 0 = 1 + pozitiveRec(xs)
    | otherwise = pozitiveRec(xs)

pozitiveComp :: [Int] -> Int
pozitiveComp l = length [ 1 | x<-l, x>0 ]


--3. Scrieti o functie care returneaza lista pozitiilor numerelor impare din lista data ca parametru
pozitiiImpareAux [] _ = []
pozitiiImpareAux (x:xs) a 
    | odd x = a : (pozitiiImpareAux xs (a+1))
    | otherwise = pozitiiImpareAux xs (a+1)

pozitiiImpareRec :: [Int] -> [Int]
pozitiiImpareRec [] = []
pozitiiImpareRec l = pozitiiImpareAux l 0


pozitiiImpareComp l = [index | (x,index) <- zip l [0..] , odd x]


--4. [MultDigit] Scrietti o functie care calculeaza produsul tuturor cifrelor care apar in sirul de caractere dat ca intrare. 
-- Daca nu sunt cifre in sir, raspunsul functiei trebuie sa fie 1.
multDigitsRec "" = 1
multDigitsRec (c:sir)
    | isDigit c = (digitToInt c) * multDigitsRec sir
    | otherwise = multDigitsRec sir

multDigitsComp :: String -> Int
multDigitsComp sir = product [ digitToInt ch | ch <- sir, isDigit ch ]


--5 [Discount] Scrieti o functie care pentru o list de valori (reprezentand niste preturi) aplica un discount 
-- de 25% acelor valori si pastreaz in list doar valorile reduse care sunt mai mici decat 200.
discountRec [] = []
discountRec (x:xs)
    | 0.75 * x < 200 = 0.75 * x : discountRec xs
    | otherwise = discountRec xs


discountComp l = [0.75 * x | x <- l, 0.75 * x < 200]


discount :: Float -> Float     
discount x = x - 0.25 * x

discountRec2 :: [Float] -> [Float]
discountRec2 [] = []
discountRec2 (x:xs) 
   | discount x < 200 =  discount x : discountRec xs
   | otherwise = discountRec xs


discountComp2 :: [Float] -> [Float]
discountComp2 xs = [ y | x<- xs, let y = discount x, y < 200]