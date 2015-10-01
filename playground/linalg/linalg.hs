import Data.Monoid

{- General Vector Datatype -}
data Vector a = Vector [a] deriving (Eq)

{- Instances -}
instance (Show a, Eq a) => Show (Vector a) where
  show (Vector c) = "Vector " ++ (show c)

instance Functor Vector where
  fmap f (Vector []) = Vector []
  fmap f (Vector c) = Vector (map f c)

{- Creation -}
vzip :: Vector a -> Vector a -> Vector (a, a)
vzip (Vector []) (Vector []) = Vector []
vzip (Vector c1) (Vector c2) = Vector (zip c1 c2)


{- Higher order functions -}
reduce :: (a -> b -> a) -> a -> Vector b -> a
reduce f a (Vector []) = a
reduce f a (Vector c) = foldl f a c

vreverse :: Vector a -> Vector a
vreverse v = Vector (reduce (\a b -> b : a) [] v)

compAt :: Int -> Vector a -> a
compAt pos (Vector v) = fst $ head firstN
    where
      firstN = dropWhile (\(a,idx) -> idx /= pos) (zip v [0..])

{- Float specific Vector functions -}
instance Num a => Monoid (Vector a) where  
  mempty = Vector []  
  Vector x `mappend` Vector y = Vector (x `mappend` y)  

type FVec = Vector Float
type FFunc = (Float -> Float -> Float)

parMap :: FFunc -> FVec -> FVec -> FVec
parMap f v1 v2 = fmap (\(a,b) -> f a b) (vzip v1 v2)

vsum :: FVec -> Float
vsum v = reduce (\a b -> a + b) 0.0 v

add :: FVec -> FVec -> FVec
add = parMap (\a b -> a + b)

sub :: FVec -> FVec -> FVec
sub = parMap (\a b -> a - b)

mul :: FVec -> FVec -> FVec
mul = parMap (\a b -> a * b)

smul :: Float -> FVec -> FVec
smul scalar v = fmap (\a -> scalar*a) v

dotProduct :: FVec -> FVec -> Float
dotProduct v1 v2 = vsum $ mul v1 v2

vlength :: FVec -> Float
vlength v = sqrt len
    where
      len = reduce (\a b -> a + b * b) 0 v

toUnit :: FVec -> FVec
toUnit v = fmap (\a -> a / size) v
    where
      size = vlength v

{- Examples Vectors -}
v1 = Vector [1.2,1.3,2.0] :: FVec
v2 = Vector [4.0,1.0,2.0] :: FVec


{- Matrix -}
data Matrix a = Matrix [[a]] deriving (Eq)

instance (Show a, Eq a) => Show (Matrix a) where
  show (Matrix c) = "Matrix(" ++ (lshow c) ++ "\n)"

instance Functor Matrix where
  fmap f (Matrix []) = Matrix []
  fmap f (Matrix as) = Matrix (map (\a -> map f a) as)

lshow :: (Show a, Eq a) => [[a]] -> String
lshow [] = ""
lshow (x:xs) = "\n  " ++ (show x) ++ (lshow xs) 


{- Float specific Vector functions -}
instance Num a => Monoid (Matrix a) where  
  mempty = Matrix []  
  Matrix x `mappend` Matrix y = Matrix (map (\(r1, r2) -> r1 `mappend` r2) (zip x y))

{- Float specific Matrice functions -}
type FMat = Matrix Float

{- Examples Matrices -}
m1 = Matrix [[1..5],[1..5],[1..5],[1..5],[1..5]] :: FMat


