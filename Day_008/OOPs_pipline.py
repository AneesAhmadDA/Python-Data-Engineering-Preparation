import pandas as pd
class pipline:
    def extraction(self,path):
        self.path=path
        df=pd.read_csv(self.path)
        print(df.head(5))
        print("***********************************************")
        print("       Extraction Done Successfully            ")
        print("***********************************************")
        return df
    def transformation(self,df):
        df=df.copy()
        print("***********************************************")
        print("         Doing the Transformation              ")
        print("***********************************************")
        print("Doing the analysis before the transformation")
        print(df.describe())
        print("      Now checking for the nulls               ")
        print(df.isnull().sum())
        print("CHecking for the Duplicate values IN PK")
        print(df[df.duplicated(subset=["transaction_id"],keep=False)])
        print("Removing the Duplicates from PK")
        df=df.drop_duplicates(subset=["transaction_id"],keep="first")
        print("Verification of DUplicates Drop")
        print(df["transaction_id"].duplicated().sum())
        print("Handling the Nulls in the coulums with the nulls ")
        for column in df.columns:
            if df[column].isnull().any():
                if pd.api.types.is_numeric_dtype(df[column]):
                    mean_value=df[column].mean()
                    df[column]=df[column].fillna(mean_value)
                    print(f"{column}:Null Values replaced with mean --> {mean_value}")
                else:
                    print(f"{column}: Non-numeric column Skipped ")
        print("Numeric missing values Handled Successfully ")
        print(df.isnull().any())
        print(" Final Statistical Summary after Transformation")
        print(df.describe())
        df.info()
        return df

    def load(self,df,output_path):
        print("***********************************************")
        print("     Loading the Data to clean csv file        ")
        print("***********************************************")
        self.output_path=output_path
        print(f"Saving the Transformed Data into the \n {self.output_path}")
        df.to_csv(self.output_path,index=False)
        print("Data Saved Successfully")
        print("***********************************************")
        print("      ETL Pipline Runs Successfully            ")
        print("***********************************************")

Data=pipline()
df=Data.extraction("C:\\Users\\pc\\OneDrive\\Documents\\Python\\Internship_prep\\Day_008\\grocery_sales_raw.csv")
df=Data.transformation(df)
Data.load(df,"Cleaned_data.csv")
        
