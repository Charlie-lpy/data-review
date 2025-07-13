# src/changes_highlighter.py

import pandas as pd

def generate_highlighted_styler(original_df, edited_df, comment_col="Comment", color_list=['yellow','lightgreen', 'lightcoral'], review_mode=False):
    """
    Generate a styled DataFrame to highlight changes between original and edited DataFrames.
    Parameters:
    - original_df: The original DataFrame.
    - edited_df: The edited DataFrame.
    - comment_col: The column used for comments (default is "Comment").
    - color_list: List of colors to use for highlighting changes.
    - review_mode: If True, applies additional logic for review mode (default is False).
    Returns:
    - styled_df: A styled DataFrame with highlighted changes.
    - suspicious_mask: A boolean mask indicating suspicious changes.
    """

    assert original_df.shape == edited_df.shape, "Both DataFrames must have the same shape."

    diff_mask = (edited_df != original_df).astype(int)

    def highlight_changes(mark):
        try:
            if mark > 0:
                color = color_list[mark-1]
                return f'background-color: {color}'
            else: 
                return ''
        except IndexError:
            return 'background-color: lightgray'  # Fallback for unexpected mark values

    suspicious_flag = False

    if review_mode:

        approved_mask = edited_df[comment_col] == "Approved"
        diff_mask.loc[approved_mask, comment_col] = 2  # Green

        row_change_count = diff_mask.drop(columns=[comment_col]).sum(axis=1)

        suspicious_mask = (
            ((row_change_count > 0) & approved_mask) |
            ((row_change_count == 0) & (diff_mask[comment_col] == 1))
        )
        diff_mask.loc[suspicious_mask, comment_col] = 3  # Red

        suspicious_flag = suspicious_mask.any()

    styled_df = edited_df.style.apply(
        lambda row: [
            highlight_changes(mark)
            for mark in diff_mask.loc[row.name]
        ],
        axis=1
    )

    return styled_df, suspicious_flag


