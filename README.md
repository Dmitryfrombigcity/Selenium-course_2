## Задачи для курса [Selenium на Python](https://stepik.org/course/188355 "https://stepik.org/course/188355").
## Каталог [Amazon](https://github.com/Dmitryfrombigcity/Selenium-course_2/tree/master/Amazon) содержит демо-программу, которая:
 + произвольно выбирает страну и пытается сделать покупки;
 + выводит лог в консоль;    
 + делает screenshots ошибок;
 + записывает cookies текущей сессии в файл;
 + последовательно выводит покупки для каждой страны.

### Начальные установки [main.py](https://github.com/Dmitryfrombigcity/Selenium-course_2/blob/master/Amazon/main.py).  
 + _quantity_of_countries_ -- количество стран;  
 + _quantity_of_purchases_ -- планируемое количество покупок на страну;
 + collect_data() -- сбор информации;
 + show_data() -- вывод корзин покупок.

### Инициализация броузера [browser.py](https://github.com/Dmitryfrombigcity/Selenium-course_2/blob/master/Amazon/browser.py).

### Модуль с базовыми методами для страницы [base.py](https://github.com/Dmitryfrombigcity/Selenium-course_2/blob/master/Amazon/base.py).    

### Модуль с основными методами для страницы [amazon.py](https://github.com/Dmitryfrombigcity/Selenium-course_2/blob/master/Amazon/amazon.py).

### Модуль с основными локаторами [locators.py](https://github.com/Dmitryfrombigcity/Selenium-course_2/blob/master/Amazon/locators.py).

### Модуль с пользовательским исключением [exception.py](https://github.com/Dmitryfrombigcity/Selenium-course_2/blob/master/Amazon/exceptions.py).

### Модуль, содержащий утилиты [utils.py](https://github.com/Dmitryfrombigcity/Selenium-course_2/blob/master/Amazon/utils.py).