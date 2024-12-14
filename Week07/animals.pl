% Các facts
Goat(goat).               % goat là một con dê
Wolf(wolf).               % wolf là một con chó sói

% Dê là động vật ăn cỏ
herbivore(goat).            

% Chó sói hung dữ
aggressive(X) :- wolf(X).

% Động vật hung dữ là động vật ăn thịt
carnivore(X) :- aggressive(X).

% Động vật ăn thịt thì ăn thịt
eats(X, meat) :- carnivore(X).

% Động vật ăn cỏ thì ăn cỏ
eats(X, grass) :- herbivore(X).

% Động vật ăn thịt thì ăn động vật ăn cỏ
eats(X, Y) :- carnivore(X), herbivore(Y).

% Động vật ăn thịt và ăn cỏ đều uống nước
drinks(X, water) :- carnivore(X); herbivore(X).

% Một động vật tiêu thụ cái nó uống hoặc ăn
consumes(X, Y) :- eats(X, Y); drinks(X, Y).

