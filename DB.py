import pandas as pd



def main():
    print("Hello, World!")



    print(DimensieProduct())


def DimensieProduct():
    import pyodbc
    import pandas as pd
    import warnings

    conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=./Databases/aenc.accdb;')
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()

    DB = {'servername': 'LAPTOP-JCB37LKM\SQLEXPRESS',
          'database': 'NorthWind'}

    export_conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+ DB['servername'] + ';DATABASE=' + DB['database'] + ';Trusted_Connection=yes')

    DB2 = {'servername': 'LAPTOP-JCB37LKM\SQLEXPRESS',
           'database': 'AdventureWorks2019'}

    export_conn_adventurewors = pyodbc.connect('DRIVER={SQL Server};SERVER='+ DB2['servername'] + ';DATABASE=' + DB2['database'] + ';Trusted_Connection=yes')

    aenc_df_product = pd.read_sql_query("SELECT * FROM product",cnxn)
    adv_df_product = pd.read_sql_query("SELECT ProductID,Name,ProductSubcategoryID from Production.Product",export_conn_adventurewors)
    adv_df_product_subcategory = pd.read_sql_query("SELECT ProductSubcategoryID,Name,ProductCategoryID from Production.ProductSubcategory",export_conn_adventurewors)
    adv_df_product_category = pd.read_sql_query("SELECT Name,ProductCategoryID from Production.ProductCategory",export_conn_adventurewors)
    nw_df_product = pd.read_sql_query("SELECT * from Products",export_conn)
    nw_df_category = pd.read_sql_query("SELECT CategoryID,CategoryName from Categories",export_conn)

    adv_product_final = adv_product_demensie(adv_df_product,adv_df_product_subcategory,adv_df_product_category)
    aenc_df_product_final = AenC_product_demensie(aenc_df_product)
    nw_df_product_final = nw_product_demensie(nw_df_product,nw_df_category)

    combined_products = pd.concat([adv_product_final, aenc_df_product_final, nw_df_product_final]).reset_index(drop=True)
    combined_products['ProductKey'] = combined_products.index + 1
    combined_products = combined_products.reindex(columns=['ProductKey','ProductID', 'Name','Subcategory','Category','Source'])
    return combined_products


def nw_product_demensie(nw_df_product,nw_df_category):
    nw_df_product_dropped = nw_df_product.drop(['Discontinued','ReorderLevel','UnitPrice','UnitsInStock','QuantityPerUnit','UnitsOnOrder','SupplierID'],axis=1)
    nw_df_product_merged = pd.merge(nw_df_product_dropped,nw_df_category,on='CategoryID',how='left')
    nw_df_product_merged = nw_df_product_merged.drop('CategoryID',axis=1)
    nw_df_product_merged['Source'] = 'NorthWind'
    nw_df_product_merged['Category'] = 'Food'
    nw_df_product_merged = nw_df_product_merged.rename(columns={
        'ProductName': 'Name',
        'CategoryName': 'Subcategory',

    })
    nw_df_product_final = nw_df_product_merged.reindex(columns=['ProductID', 'Name','Subcategory','Category','Source'])
    return nw_df_product_final;

def AenC_product_demensie(aenc_df_product):
    aenc_df_product_dropped = aenc_df_product.drop(['picture_name','quantity','prod_size','unit_price'],axis=1)
    aenc_df_product_dropped['Source'] = 'AenC'
    aenc_df_product_dropped = aenc_df_product_dropped.rename(columns={
        'id': 'ProductID',
        'name': 'Subcategory',
        'description': 'Name',
        'color': 'Color',

    })
    aenc_df_product_dropped['Category'] = aenc_df_product_dropped['Category'].replace('Clothes', 'Clothing')

    aenc_df_product_final = aenc_df_product_dropped.reindex(columns=['ProductID', 'Name', 'Subcategory','Category','Source'])

    return aenc_df_product_final

def adv_product_demensie(adv_df_product,adv_df_product_subcategory,adv_df_product_category):
    adv_product_merged = pd.merge(adv_df_product,adv_df_product_subcategory,on='ProductSubcategoryID',how='left')
    adv_product_merged = pd.merge(adv_product_merged,adv_df_product_category,on='ProductCategoryID',how='left')

    adv_product_merged = adv_product_merged.drop(['ProductSubcategoryID','ProductCategoryID'],axis=1)
    adv_product_merged = adv_product_merged.rename(columns={
        'Name': 'Category',
        'Name_y': 'Subcategory',
        'Name_x': 'Name',
    })
    adv_product_merged['Source'] = 'AdventureWorks'
    adv_product_final = adv_product_merged.reindex(columns=['ProductID', 'Name', 'Subcategory','Category','Source'])

    return adv_product_final



if __name__ == "__main__":
    main()


