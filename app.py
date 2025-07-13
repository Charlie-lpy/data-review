import streamlit as st
import pandas as pd
import io
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from src.changes_highliter import generate_highlighted_styler

st.set_page_config(
    page_title="Data Review Tool",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 Data Review Tool")

tab1, tab2, tab3 = st.tabs(["Report Customizer","Data Review", "Changes Highlighter"])

with tab1:

    original_report = st.file_uploader("Upload Original Report (Excel)", type=["xlsx"], key="original_report")
    template_report = st.file_uploader("Upload Template Report (Excel)", type=["xlsx"], key="template_report")

    if original_report and template_report:
        original_df = pd.read_excel(original_report)
        template_df = pd.read_excel(template_report)

        # Reorder columns based on template
        new_df = original_df[template_df.columns]

        # Save the new DataFrame to a BytesIO buffer
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            new_df.to_excel(writer, index=False)
        buffer.seek(0)

        st.subheader("Customized Report")
        st.dataframe(new_df, use_container_width=True)

        st.download_button(
            label="📥 Download Customized Report",
            data=buffer,
            file_name="customized_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


with tab2:
                 
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df.reset_index(drop=True, inplace=True)

        # Add 'Comment' column if not exists (in first column)
        if 'Comment' not in df.columns:
            df.insert(0, 'Comment', 'Pending')
        
        # Keep a copy to compare changes later
        original_df = df.copy()

        # --------------------------------------------
        # 1. Show Original Data (read-only)
        # --------------------------------------------
        with st.expander("🧾 Show Original Data (Read-only)", expanded=True):
            st.dataframe(original_df, use_container_width=True)

        # --------------------------------------------
        # 2. Show Editable Data with Dropdown
        # --------------------------------------------
        st.subheader("✏️ Edit Data")
        edited_df = st.data_editor(
            df,
            num_rows="fixed",
            key="data_editor",
            disabled=["Confirmation Number"],  # Disable editing of Confirmation Number
            column_config={
                "Comment": st.column_config.SelectboxColumn(
                    label="Comment",
                    options=["Pending", "Approved", "Approved with Changes", "Needs Change"],
                    required=True
                )
            },
            use_container_width=True
        )

        # --------------------------------------------
        # 3. Highlight Changes
        # --------------------------------------------
        st.subheader("🔍 Highlight Differences")

        styled_df, suspicious_flag = generate_highlighted_styler(
            original_df,
            edited_df,
            comment_col="Comment",
            color_list=['yellow', 'lightgreen', 'lightcoral'],
            review_mode=True
        )

        st.dataframe(styled_df, use_container_width=True)
        # st.markdown(styled_df.to_html(), unsafe_allow_html=True)


        if suspicious_flag:
            st.warning("⚠️ Some rows have suspicious changes. Please review them carefully.")
        else:
            # Filter by comment type
            pending_df = pd.DataFrame()
            approved_df = pd.DataFrame()
            approved_with_changes_df = pd.DataFrame()
            needs_change_df = pd.DataFrame()

            pending_df = edited_df[edited_df['Comment'] == 'Pending']
            approved_df = edited_df[edited_df['Comment'] == 'Approved']
            approved_with_changes_df = edited_df[edited_df['Comment'] == 'Approved with Changes']
            needs_change_df = edited_df[edited_df['Comment'] == 'Needs Change']

            # download into an excel with multiple sheets
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                original_df.to_excel(writer, sheet_name='Original Data', index=True)
                edited_df.to_excel(writer, sheet_name='Edited Data', index=False)
                pending_df.to_excel(writer, sheet_name='Pending', index=False)
                approved_df.to_excel(writer, sheet_name='Approved', index=False)
                approved_with_changes_df.to_excel(writer, sheet_name='Approved with Changes', index=False)
                needs_change_df.to_excel(writer, sheet_name='Needs Change', index=False)
            buffer.seek(0)

            # Download button
            st.download_button(
                label="📥 Download Updated Data",
                data=buffer,
                file_name="updated_data_with_comments.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

with tab3:

    original_file_loaded = st.file_uploader(
        "Upload Original Data (Excel)",
        type=["xlsx"],
        key="original_file"
    )

    edited_file_loaded = st.file_uploader(
        "Upload Edited Data (Excel)",
        type=["xlsx"],
        key="edited_file"
    )

    if original_file_loaded and edited_file_loaded:
        original_df = pd.read_excel(original_file_loaded)
        edited_df = pd.read_excel(edited_file_loaded)

        styled_df, suspicious_flag = generate_highlighted_styler(
            original_df,
            edited_df,
            color_list=['yellow', 'lightgreen', 'lightcoral'],
            review_mode=False
        )

        st.subheader("🔍 Highlight Changes")
        st.dataframe(styled_df, use_container_width=True)

