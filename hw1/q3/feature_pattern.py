import numpy as np
import pandas as pd
import shap
import sys
import time
from sklearn.linear_model import LogisticRegression, LassoCV
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE, SelectKBest, chi2, mutual_info_classif, VarianceThreshold
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import csv

# Function to remove correlated features
def remove_correlated_features(X, threshold=0.9):
    corr_matrix = X.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    return X.drop(columns=to_drop, errors='ignore')

# Function to perform feature selection
def feature_selection(X, y, max_features=100):
    selector = VarianceThreshold(threshold=0.01)
    X = X.loc[:, selector.fit(X).get_support()]

    # Mutual Information
    mi = mutual_info_classif(X, y)
    selected_mi = X.columns[np.argsort(mi)[-max_features:]]

    # Chi-Square (Handling Exception)
    try:
        chi2_selector = SelectKBest(chi2, k=min(max_features, X.shape[1]))
        chi2_selector.fit(X, y)
        selected_chi2 = X.columns[chi2_selector.get_support()]
    except:
        selected_chi2 = []

    # Recursive Feature Elimination (RFE)
    model_rfe = LogisticRegression(max_iter=10000, solver='liblinear')
    rfe = RFE(model_rfe, n_features_to_select=min(max_features, X.shape[1]))
    rfe.fit(X, y)
    selected_rfe = X.columns[rfe.support_]

    # Lasso (L1 Regularization)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    lasso = LassoCV(cv=5, max_iter=10000)
    lasso.fit(X_scaled, y)
    selected_lasso = X.columns[lasso.coef_ != 0]

    selected_features = set(selected_mi).union(set(selected_rfe), set(selected_lasso), set(selected_chi2))
    return list(selected_features)[:max_features]

# Function for ensemble feature selection
def eslr_feature_selection(input_csv_file, output_csv_file, max_features=100):
    df = pd.read_csv(input_csv_file)
    X = df.drop(columns=['TID', 'Label'])
    y = df['Label']

    # Handle class imbalance
    smote = SMOTE()
    X, y = smote.fit_resample(X, y)

    # Remove correlated features
    X = remove_correlated_features(X)

    # Perform Feature Selection
    selected_features = feature_selection(X, y, max_features)
    X_selected = X[selected_features]

    # Compute SHAP feature importance
    model = LogisticRegression(max_iter=10000, solver='liblinear')
    model.fit(X_selected, y)
    explainer = shap.Explainer(model, X_selected)
    shap_values = explainer(X_selected)
    feature_importance_shap = np.abs(shap_values.values).mean(axis=0)

    # Rank features by SHAP importance
    sorted_features = sorted(
        zip(selected_features, feature_importance_shap), key=lambda x: x[1], reverse=True
    )
    selected_features_final = [feature for feature, _ in sorted_features[:max_features]]

    # Save selected features
    selected_df = df[['TID'] + selected_features_final]
    selected_df.to_csv(output_csv_file, index=False)

    # Save selected feature names to a text file
    with open("selected_features.txt", "w") as f:
        for feature in selected_features_final:
            f.write(feature + "\n")

    return selected_features_final

# Function to extract patterns from the graph file
def extract_patterns(features_file, input_file_path, output_file_path):
    with open(features_file, 'r') as f:
        input_list = [line.strip() for line in f.readlines()]  # Read features as a list

    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    output_content = []
    for item in input_list:
        item_cleaned = item.strip("'")  # Clean the feature name
        pattern_found = False

        for i, line in enumerate(lines):
            if f"t # {item_cleaned}," in line:
                output_content.append(line.strip())
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith("t #"):
                        break
                    output_content.append(lines[j].strip())
                pattern_found = True
                break

        if not pattern_found:
            print(f"Pattern {item_cleaned} not found in the input file.")

    with open(output_file_path, 'w') as file:
        file.write("\n".join(output_content))

    print(f"Extracted patterns saved to {output_file_path}")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_csv> <input_graph_file> <output_file>")
        sys.exit(1)

    start_time = time.time()
    
    input_csv = sys.argv[1]   # Example: 'input.csv'
    input_graph_file = sys.argv[2]  # Example: 'pre_proc.fp'
    output_file = sys.argv[3]  # Example: 'disc_subg1.txt'

    selected_features = eslr_feature_selection(input_csv, "selected_features.csv")
    extract_patterns("selected_features.txt", input_graph_file, output_file)

    print(f"Total Execution Time: {time.time() - start_time:.2f} seconds")
