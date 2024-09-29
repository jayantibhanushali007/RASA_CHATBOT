# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# this data was simulated using script : data_simulate.py
# if you want to make it more complex with more details and variations 
# feel free to do so

import pandas as pd 

catalogue={'Phone':['iphone','samsung','oneplus','mi','oppo','nokia'],
          'TV':['apple','sony','hitachi','LG','philips'],
          'Laptop':['lenovo','hp','dell','acer','asus'],
          'Camera': ['nikon','canon','fujifilm','panasonic']}

data_file='C:/Users/Jayanti/Documents/Edvancer/Deep Learning - 6th July 2024/10 - Chatbots/proj_2/cust_orders.csv'
cust_orders=pd.read_csv(data_file)

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List


from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction

def _find_order_status(customerId,orderID):
    print(customerId,orderID)
    order_info=cust_orders[(cust_orders['customer_id']==customerId) & (cust_orders['order_id']==orderID)]
    print(order_info)
    try:
        print('finding the order')
        results=order_info[['quantity','product','brand','order_date','expected_arrival','status']]
        print('returned results')
        print(results)
        return(results)
    except:
        return False

def _get_new_orderid(customerId):


	temp=cust_orders.sort_values(['customer_id','order_date']).groupby(['customer_id']).tail(1)
	last_oid=temp[temp['customer_id']==customerId]['order_id']

	new_oid='o'+str(int(last_oid[1:])+1)

	return new_oid

def _remove_order(customerId,orderID):

	temp=cust_orders[cust_orders['customer_id']==customerId]
	order=orderID.isin(temp['order_id'])

	if order:
		cust_orders=cust_orders[~((cust_orders['customer_id']==customerId) & (cust_orders['order_id']==orderID))]

	return order

class FindOrderStatus(Action):
    """This action class retrieves the order status."""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "find_order_status"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:

        customerId = tracker.get_slot("customerId")
        orderID = tracker.get_slot("orderID")

        if customerId is None:
        	dispatcher.utter_message(f'''can you please help me with your customer id''')

        if orderID is None:
        	dispatcher.utter_message(f'''can you please help me with your order id''')

        customerId = tracker.get_slot("customerId")
        orderID = tracker.get_slot("orderID")

        details=_find_order_status(customerId,orderID)


        if details is not None:
        	dispatcher.utter_message(f''' you placed an order for {details['quantity'].values} {details['product'].values} 
 					of brand {details['brand'].values} on {details['order_date'].values}. expected
					delivery date given to you was {details['expected_arrival'].values}. 
					current status of the order is {details['status'].values}''')
        else :
        	dispatcher.utter_message(f'''sorry i could not find an order on your account with  order id {orderID}. 
        		can you please recheck that ''')

        
class PlaceOrder(Action):
    """This action class retrieves the order status."""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "place_order"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:

        customerId = tracker.get_slot("customerId")
     
        product=tracker.get_slot('product')
        brand=tracker.get_slot('brand')
        quantity=tracker.get_slot('quantity')
        paymentMethod=tracker.get_slot('payment_method')

        if customerId is None:
        	dispatcher.utter_message('''can you please help me with your customer id''')

        
       	if product is None:
        	dispatcher.utter_message(f'''what would you like to order from this list of
        	 							products : {list(catalogue.keys())}''')
        
        if brand is None:
        	dispatcher.utter_message(f'''what brand would you prefer here : 
        				{list(catalogue[product])}''')
        if quantity is None:
        	dispatcher.utter_message(f'''you can order upto 3 {product} . how many would you like to order?''')
        if paymentMethod is None:
        	dispatcher.utter_message(f'''how would you like to pay for this ? COD or Online on delivery?''')

        customerId = tracker.get_slot("customerId")
        orderID = tracker.get_slot("orderID")
        product=tracker.get_slot('product')
        brand=tracker.get_slot('brand')
        quantity=tracker.get_slot('quantity')
        paymentMethod=tracker.get_slot('payment_method')
        
        order={}
        order['customer_id']=customerId

        order['order_id']=_get_new_orderid(customerId)
        
        order_on=pd.to_datetime('now').date()
        order['order_date']=order_on
    
        order['product']=product
        order['brand']=brand
        order['status']='sent_for_dispatch'
        order['expected_arrival']=order['ordered_on']+10*np.random.choice([0.1,0.2,0.3],1)[0]
        order['payment_method']=payment_method
        order['quantity']=quantity
        
        d=pd.DataFrame(order)
        
        db=pd.concat([cust_orders,d],0)
        

        
        dispatcher.utter_message(f''' you placed an order for {quantity} {product} of 
        	brand {brand}  today. expected delivery date is 
        	 is {order['expected_arrival']}. ''')
        
class CancelOrder(Action):
    """This action class retrieves the order status."""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "cancel_order"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:

        customerId = tracker.get_slot("customerId")
        orderID = tracker.get_slot("orderID")

        if customerId is None:
        	dispatcher.utter_message(f'''can you please help me with your customer id''')

        if orderID is None:
        	dispatcher.utter_message(f'''can you please help me with your order id''')

        customerId = tracker.get_slot("customerId")
        orderID = tracker.get_slot("orderID")

        result=_remove_order(customerId,orderID)


        if result is not None:
        	dispatcher.utter_message(f''' your order has been cancelled''')
        else :
        	dispatcher.utter_message(f'''sorry i could not find an order on your account with  
        		order id {orderID}.can you please recheck that ''')


