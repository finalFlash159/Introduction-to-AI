% Võ Minh Thịnh
% MSSV: 22280087

parent(marry,bill).
parent(tom,bill).
parent(tom,liz).
parent(bill,ann).
parent(bill,sue).
parent(sue,jim).


% 1. Cho quan hệ parent như trong phần II, cho biết kết quả của các câu hỏi sau:
% a. ?- parent(jim, X). 
% false.
% b. ?- parent(X, jim).
% X = sue.
% c. ?- parent(marry, X), parent(X, part).
% false.
% d. ?- parent(marry, X), parent(X, Y), parent(Y, jim).
% X = bill, 
% Y = sue.

% 2. Viết các Mệnh đề Prolog diễn tả các câu hỏi liên quan đến quan hệ parent:
% a. Ai là cha Mẹ của Bill ?
% ?- parent(X, bill), parent(Y, bill), X\=Y.
% X = marry,
% Y = tom .
% => cha mẹ của bill là marry và tom

% b. Marry có con không ?
% ?- parent(marry,X).
% X = bill.
% => marry có con là bill

% c. Ai là ông bà (grandparent) của Sue ?
% ?- parent(X, sue), parent(Y, X), parent(Z, X), Z\=Y.
% X = bill,
% Y = marry,
% Z = tom.
% => bill là parent của sue => marry và tom và grandparent của sue