CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    email Varchar(60) NOT NULL UNIQUE,
    password VARCHAR(120),
    date_of_birth DATE,
    user_type VARCHAR(20)
);


CREATE TABLE meals
(
    id SERIAL PRIMARY KEY,
    meal_name VARCHAR(30),
    meal_Type VARCHAR(50),
    cooking_time INT,
    image_path VARCHAR(50)
);


CREATE TABLE user_meals
(
    user_id INT,
    meal_id INT,
    CONSTRAINT user_meals_ufk FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT user_meals_mfk FOREIGN KEY (meal_id) REFERENCES meals(id),
    CONSTRAINT user_meals_pk PRIMARY KEY (user_id, meal_id)
);

INSERT INTO users values (DEFAULT, 'Jordan May', 'jordanmay21@gmail.com', 'pbkdf2:sha256:260000$7PpaxKKNooMrgSFN$f991742f184a538568ba16670422564cf3b4f0c3877a4a305666c93f64f6f399', TO_DATE('04/02/1993','DD/MM/YYYY'), 'STANDARD');
INSERT INTO users values (DEFAULT, 'Madison Bear', 'MaddyBaddy42@gmail.com', 'pbkdf2:sha256:260000$NxptfKWzuMJG6fR2$18983214c8a36d8cd5d12716fc1fd4aad17b0c50f2832ce6f51aba7109f37483', TO_DATE('24/12/1998','DD/MM/YYYY'), 'STANDARD');
INSERT INTO users values (DEFAULT, 'Meghan Simons', 'MeghanS1995@gmail.com', 'pbkdf2:sha256:260000$bI7Wb6JQkoV70qHj$9141eab3baf759b94e33919a969ee347f335dc45b05974ad7f584af18cfb0c05', TO_DATE('12/02/1995','DD/MM/YYYY'), 'ADMIN');
INSERT INTO users values (DEFAULT, 'Joe Anderson', 'joedAnderson31@gmail.com', 'pbkdf2:sha256:260000$vd4R5uNdQWxPtTmu$1d6b0daba0cef5581b5cf4a6d30c9f5c0ba594da34312449aff953ab375ee51f', TO_DATE('14/04/1991','DD/MM/YYYY'), 'ADMIN');
INSERT INTO users values (DEFAULT, 'Alan Castro', 'castroAlan12@gmail.com', 'pbkdf2:sha256:260000$b2o7qggtm9fUT0hh$a159ed7ea62be10505d4a7d0c4b22b5eee89aaa63a08b3c7a0d9fe64e65205f9', TO_DATE('04/02/1993','DD/MM/YYYY'), 'STANDARD');
INSERT INTO users values (DEFAULT, 'admin', 'admin@admin.com', 'pbkdf2:sha256:260000$gslHXkwZuff1nk4s$ae9c18c82cfef3e73b880633869457645e1d7439969a96d1ec8e57adf0d71ded', TO_DATE('04/02/1993','DD/MM/YYYY'), 'ADMIN');

INSERT INTO meals values (DEFAULT, 'Pizza', 'High carbs', 60, 'pizza.jpg');
INSERT INTO meals values (DEFAULT, 'Chicken', 'High protein', 30, 'chicken.jpg');
INSERT INTO meals values (DEFAULT, 'Fish', 'High protein', 60, 'fish.jpg');
INSERT INTO meals values (DEFAULT, 'Halloumi salad', 'vegetarian', 30, 'halloumi.jpg');
INSERT INTO meals values (DEFAULT, 'Burger and fries', 'High carbs', 30, 'burger.jpg');
INSERT INTO meals values (DEFAULT, 'Philly cheesesteak', 'High protein', 30, 'philly.jpg');
INSERT INTO meals values (DEFAULT, 'Tofu salad', 'vegetarian', 30, 'tofu.jpg');
INSERT INTO meals values (DEFAULT, 'Caesar salad', 'vegetarian', 30, 'caesar.jpg');
INSERT INTO meals values (DEFAULT, 'vegetable curry', 'vegetarian', 60, 'veg_curry.jpg');
INSERT INTO meals values (DEFAULT, 'chicken curry', 'vegetarian', 60, 'chicken_curry.jpg');



INSERT INTO user_meals values (2,2);
INSERT INTO user_meals values(1,2);
commit;



