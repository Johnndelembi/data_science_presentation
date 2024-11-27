import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

class DataAnalyzer:
    def __init__(self, file_path):
        """Initialize the DataAnalyzer with the path to CSV file"""
        self.file_path = file_path
        self.df = None
        self.numeric_columns = None
        self.categorical_columns = None
    
    def load_data(self):
        """Load the CSV file into a pandas DataFrame"""
        try:
            self.df = pd.read_csv(self.file_path)
            print("Data loaded successfully!")
            print(f"Shape of dataset: {self.df.shape}")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def clean_data(self):
        """Clean the data by handling missing values and duplicates"""
        # Store original shape
        original_shape = self.df.shape
        
        # Remove duplicates
        self.df.drop_duplicates(inplace=True)
        
        # Identify numeric and categorical columns
        self.numeric_columns = self.df.select_dtypes(include=['int64', 'float64']).columns
        self.categorical_columns = self.df.select_dtypes(include=['object']).columns
        
        # Handle missing values
        numeric_imputer = SimpleImputer(strategy='mean')
        categorical_imputer = SimpleImputer(strategy='most_frequent')
        
        if len(self.numeric_columns) > 0:
            self.df[self.numeric_columns] = numeric_imputer.fit_transform(self.df[self.numeric_columns])
        
        if len(self.categorical_columns) > 0:
            self.df[self.categorical_columns] = categorical_imputer.fit_transform(self.df[self.categorical_columns])
        
        print(f"Data cleaning complete!")
        print(f"Original shape: {original_shape}, New shape: {self.df.shape}")

    def descriptive_analysis(self):
        """Perform descriptive statistical analysis"""
        print("\n=== Descriptive Statistics ===")
        
        # Numeric columns analysis
        if len(self.numeric_columns) > 0:
            print("\nNumeric Variables Summary:")
            print(self.df[self.numeric_columns].describe())
            
            # Adjust figure size and spacing
            n_cols = len(self.numeric_columns)
            n_rows = (n_cols + 1) // 2
            plt.figure(figsize=(15, 5 * n_rows))  # Increased figure size
            for i, col in enumerate(self.numeric_columns, 1):
                plt.subplot(n_rows, 2, i)
                sns.histplot(self.df[col], kde=True)
                plt.title(f'Distribution of {col}')
            plt.subplots_adjust(hspace=0.5, wspace=0.3)  # Add spacing between subplots
            plt.show()
        
        # Categorical columns analysis
        if len(self.categorical_columns) > 0:
            print("\nCategorical Variables Summary:")
            for col in self.categorical_columns:
                print(f"\nFrequency distribution for {col}:")
                print(self.df[col].value_counts())
                
                # Create bar plots for categorical variables
                plt.figure(figsize=(8, 4))
                sns.countplot(data=self.df, x=col)
                plt.title(f'Distribution of {col}')
                plt.xticks(rotation=45)
                plt.show()

    def correlation_analysis(self):
        """Perform correlation analysis for numeric variables"""
        if len(self.numeric_columns) > 1:
            print("\n=== Correlation Analysis ===")
            correlation_matrix = self.df[self.numeric_columns].corr()
            
            # Create correlation heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
            plt.title('Correlation Matrix')
            plt.show()

    def inferential_analysis(self):
        """Perform basic inferential statistical analysis"""
        print("\n=== Inferential Analysis ===")
        
        # Normality test for numeric variables
        for col in self.numeric_columns:
            stat, p_value = stats.normaltest(self.df[col])
            print(f"\nNormality test for {col}:")
            print(f"p-value: {p_value:.4f}")
            print("Conclusion: ", "Normal distribution" if p_value > 0.05 else "Not normal distribution")
        
        # If we have categorical variables, perform chi-square test
        if len(self.categorical_columns) >= 2:
            for i in range(len(self.categorical_columns)):
                for j in range(i+1, len(self.categorical_columns)):
                    col1, col2 = self.categorical_columns[i], self.categorical_columns[j]
                    contingency_table = pd.crosstab(self.df[col1], self.df[col2])
                    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
                    print(f"\nChi-square test between {col1} and {col2}:")
                    print(f"p-value: {p_value:.4f}")
                    print("Conclusion: ", "Dependent" if p_value < 0.05 else "Independent")

def main():
    # Initialize and run analysis
    analyzer = DataAnalyzer('your_data.csv')
    
    if analyzer.load_data():
        analyzer.clean_data()
        analyzer.descriptive_analysis()
        analyzer.correlation_analysis()
        analyzer.inferential_analysis()

if __name__ == "__main__":
    main()