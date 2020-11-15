import Data.Char
import Data.List


-- 1.
rotate :: Int -> [Char] -> [Char]
rotate n str
    | n < 0 = error "n is negative"
    | n > length str = error "n is greater than the lenght of the given string"
    | otherwise = (drop n str) ++ (take n str)

-- 2.
prop_rotate :: Int -> String -> Bool
prop_rotate k str = rotate (l - m) (rotate m str) == str
                        where l = length str
                              m = if l == 0 then 0 else k `mod` l

-- 3.
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
makeKey :: Int -> [(Char, Char)]
makeKey n = zip alphabet (rotate n alphabet)

-- 4.
lookUp :: Char -> [(Char, Char)] -> Char
lookUp ch [] = ch
lookUp ch ((a,b):xs) = if ch == a then b else lookUp ch xs
-- lookUp ch str = fmap snd (find (\(x, _) -> x == ch) str)

-- 5.
encipher :: Int -> Char -> Char
encipher n ch = lookUp ch (makeKey n)

-- 6.
normalize :: String -> String
normalize str = filter isAlphaNum  (map toUpper str)

-- 7.
encipherStr :: Int -> String -> String
encipherStr n str = map (encipher n) (normalize str)

-- 8.
reverseKey :: [(Char, Char)] -> [(Char, Char)]
reverseKey = map(\(x,y) -> (y,x))

-- 9.
decipher :: Int -> Char -> Char
decipher n ch = lookUp ch (reverseKey (makeKey n)) 

decipherStr :: Int -> String -> String
decipherStr n = map  (decipher n) . normalize