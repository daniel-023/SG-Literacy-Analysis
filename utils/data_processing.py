import pandas as pd


def process_data(df):
    """
    Transform the original dataframe into format ready for classification
    """
    # Remove summary rows
    cleaned_df = df[
        ~(df['Language Literacy'].isin(['Total', 'Literate'])) &
        ~(df['Qualification'] == 'Total') &
        ~(df['Gender'] == 'Total') &
        ~(df['Language Literacy'].isin(['One Language Only', 'Two Languages Only', 'Three or More Languages']))
    ].copy()

    # Create number of languages feature
    def categorize_language_count(x):
        if x == 'Not Literate':
            return 0
        elif x in('English Only', 'Chinese Only', 'Malay Only', 'Tamil Only', 'Non-Official Language Only'):
            return 1
        elif x in('English & Chinese Only', 'English & Malay Only', 'English & Tamil Only', 'English & Non-Official Language Only', 'Other Two Languages Only'):
            return 2
        elif x in('English, Chinese & Malay Only', 'English, Malay & Tamil Only', 'Other Three or More Languages'):
            return 3
        else:
            print(f"WARNING: Uncategorized language literacy value: {x}")
            return None

    cleaned_df['num_languages'] = cleaned_df['Language Literacy'].apply(categorize_language_count)

    # Create education level encoding
    education_order = {
        'No Qualification': 0,
        'Primary': 1,
        'Lower Secondary': 2,
        'Secondary': 3,
        'Post-Secondary (Non-Tertiary)': 4,
        'Polytechnic Diploma': 5,
        'Professional Qualification and Other Diploma': 6,
        'University': 7
    }
    cleaned_df['education_level_ordinal'] = cleaned_df['Qualification'].map(education_order)

    # Create gender encoding
    cleaned_df['gender_numeric'] = (cleaned_df['Gender'] == 'Males').astype(int)

    # Create language features
    cleaned_df['eng_speaker'] = cleaned_df['Language Literacy'].str.contains('English').astype(int)
    cleaned_df['chi_speaker'] = cleaned_df['Language Literacy'].str.contains('Chinese').astype(int)
    cleaned_df['malay_speaker'] = cleaned_df['Language Literacy'].str.contains('Malay').astype(int)
    cleaned_df['tamil_speaker'] = cleaned_df['Language Literacy'].str.contains('Tamil').astype(int)

    # Group percentages
    cleaned_df['total_per_group'] = cleaned_df.groupby(['education_level_ordinal', 'gender_numeric'])['Count'].transform('sum')
    cleaned_df['percentage'] = (cleaned_df['Count'] / cleaned_df['total_per_group']) * 100

    return cleaned_df

if __name__ == "__main__":
    df = pd.read_csv('data/raw_data.csv')
    processed_df = process_data(df)
    processed_df.to_csv('data/processed_data.csv', index=False)