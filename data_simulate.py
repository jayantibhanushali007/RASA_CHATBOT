import numpy as np
import random
import pandas as pd

custids=['C'+str(i) for i in range(1,11)]
num_orders=[np.random.choice(range(2,10),1)[0] for _ in custids]


catalogue={'Phone':['iphone','samsung','oneplus','mi','oppo','nokia'],
          'TV':['apple','sony','hitachi','LG','philips'],
          'Laptop':['lenovo','hp','dell','acer','asus'],
          'Camera': ['nikon','canon','fujifilm','panasonic']}

db=pd.DataFrame({'customer_id':['dummy'],'order_id':[0],'ordered_on':[pd.to_datetime('now').date()],
                 'product':['dummy'],
                 'brand':['dummy'],'status':['dummy'],'expected_arrival':[pd.to_datetime('now').date()],
                 'payment_method':['dummy'],'quantity':[0]
    })

for cid,numod in zip(custids,num_orders):
    start=pd.to_datetime('01-01-2020').date()
    end=pd.to_datetime('29-02-2020').date()
    for od in range(1,numod+1):
        order={}
        order['customer_id']=cid
        order['order_id']=od
        
        order_on=start+(end-start)*np.random.choice([0.01,0.03,0.05,0.1],1)[0]
        order['ordered_on']=order_on
    
        start=order_on
        order['product']=np.random.choice(list(catalogue.keys()),1)
        order['brand']=np.random.choice(catalogue[order['product'][0]],1)[0]
        order['status']=np.random.choice(['delivered','in_transit','sent_for_dispatch'],1)[0]
        order['expected_arrival']=order['ordered_on']+(end-start)*np.random.choice([0.1,0.2,0.3],1)[0]
        order['payment_method']=np.random.choice(['cod','onlineod'],1)[0]
        order['quantity']=np.random.choice([1,2,3],1)[0]
        
        d=pd.DataFrame(order)
        
        db=pd.concat([db,d],0)

db=db.iloc[1:,:]

db.to_csv('cust_orders.csv',index=False)