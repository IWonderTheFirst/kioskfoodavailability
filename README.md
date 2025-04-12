# Kiosk Food Availability Application
 Code by Riku Ishihara, Data Creation & Management by Kaito Nonaka

 ## Application usage
The application consists of two inputs: The product name and the stock. Using these two pieces of information, the application will create a graph estimating the stock of the product for a time. In the future, a feature will be implemented that will make the kiosk products selectable.

 ## How to use
This application can only run with the 1 million transaction data. To use this, have this python script in the same directory as the 1 million transaction data, renamed as "data.csv".

Because the transaction data surpassed the data limit of GitHub upload, I couldn't upload the data here.

## Purpose
Me and Kaito believed that in the Kiosk, products such as the BLT and Onigiri weren't avaiablle at certain periods. To allow students and faculty to buy products before they run out of stock, we developed this application that allows the user to determine the perfect time to buy their desired product. 

## How it works
The code uses the following libraries: PYQT5, Pandas, SYS, and Matploblib. The graph was calculated using the data from the transaction, and is the "average".
