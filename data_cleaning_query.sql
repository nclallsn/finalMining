-- Column name standardization
-- Prints query that convert column header with capital letters to lower case
SELECT
    'EXEC sp_rename ''[ddos_sampled_db].[dbo].[sampled_500k_dataset].['
    + COLUMN_NAME + ']'', '''
    + LOWER(COLUMN_NAME) + ''', ''COLUMN'';' AS rename_command
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'sampled_500k_dataset'
ORDER BY ORDINAL_POSITION;

-- Drop Duplicate/redundant columns
-- Prints the number of matches
SELECT
    COUNT(*) AS Total_Rows,

    SUM(CASE WHEN Total_Fwd_Packets = Subflow_Fwd_Packets THEN 1 ELSE 0 END) AS Total_Fwd_Packets_Subflow_Fwd_Packets_Matches,
    SUM(CASE WHEN Total_Backward_Packets = Subflow_Bwd_Packets THEN 1 ELSE 0 END) AS Total_Backward_Packets_Subflow_Bwd_Packets_Matches,

    SUM(CASE WHEN Bwd_PSH_Flags = Bwd_URG_Flags THEN 1 ELSE 0 END) AS Bwd_PSH_Flags_Bwd_URG_Flags_Matches,
    SUM(CASE WHEN Bwd_PSH_Flags = Fwd_Avg_Bytes_Bulk THEN 1 ELSE 0 END) AS Bwd_PSH_Flags_Fwd_Avg_Bytes_Bulk_Matches,
    SUM(CASE WHEN Bwd_PSH_Flags = Fwd_Avg_Packets_Bulk THEN 1 ELSE 0 END) AS Bwd_PSH_Flags_Fwd_Avg_Packets_Bulk_Matches,
    SUM(CASE WHEN Bwd_PSH_Flags = Fwd_Avg_Bulk_Rate THEN 1 ELSE 0 END) AS Bwd_PSH_Flags_Fwd_Avg_Bulk_Rate_Matches,
    SUM(CASE WHEN Bwd_PSH_Flags = Bwd_Avg_Bytes_Bulk THEN 1 ELSE 0 END) AS Bwd_PSH_Flags_Bwd_Avg_Bytes_Bulk_Matches,
    SUM(CASE WHEN Bwd_PSH_Flags = Bwd_Avg_Packets_Bulk THEN 1 ELSE 0 END) AS Bwd_PSH_Flags_Bwd_Avg_Packets_Bulk_Matches,
    SUM(CASE WHEN Bwd_PSH_Flags = Bwd_Avg_Bulk_Rate THEN 1 ELSE 0 END) AS Bwd_PSH_Flags_Bwd_Avg_Bulk_Rate_Matches,

    SUM(CASE WHEN Bwd_URG_Flags = Fwd_Avg_Bytes_Bulk THEN 1 ELSE 0 END) AS Bwd_URG_Flags_Fwd_Avg_Bytes_Bulk_Matches,
    SUM(CASE WHEN Bwd_URG_Flags = Fwd_Avg_Packets_Bulk THEN 1 ELSE 0 END) AS Bwd_URG_Flags_Fwd_Avg_Packets_Bulk_Matches,
    SUM(CASE WHEN Bwd_URG_Flags = Fwd_Avg_Bulk_Rate THEN 1 ELSE 0 END) AS Bwd_URG_Flags_Fwd_Avg_Bulk_Rate_Matches,
    SUM(CASE WHEN Bwd_URG_Flags = Bwd_Avg_Bytes_Bulk THEN 1 ELSE 0 END) AS Bwd_URG_Flags_Bwd_Avg_Bytes_Bulk_Matches,
    SUM(CASE WHEN Bwd_URG_Flags = Bwd_Avg_Packets_Bulk THEN 1 ELSE 0 END) AS Bwd_URG_Flags_Bwd_Avg_Packets_Bulk_Matches,
    SUM(CASE WHEN Bwd_URG_Flags = Bwd_Avg_Bulk_Rate THEN 1 ELSE 0 END) AS Bwd_URG_Flags_Bwd_Avg_Bulk_Rate_Matches,

    SUM(CASE WHEN Fwd_Header_Length = Fwd_Header_Length_1 THEN 1 ELSE 0 END) AS Fwd_Header_Length_Fwd_Header_Length_1_Matches,

    SUM(CASE WHEN Fwd_Avg_Bytes_Bulk = Fwd_Avg_Packets_Bulk THEN 1 ELSE 0 END) AS Fwd_Avg_Bytes_Bulk_Fwd_Avg_Packets_Bulk_Matches,
    SUM(CASE WHEN Fwd_Avg_Bytes_Bulk = Fwd_Avg_Bulk_Rate THEN 1 ELSE 0 END) AS Fwd_Avg_Bytes_Bulk_Fwd_Avg_Bulk_Rate_Matches,
    SUM(CASE WHEN Fwd_Avg_Bytes_Bulk = Bwd_Avg_Bytes_Bulk THEN 1 ELSE 0 END) AS Fwd_Avg_Bytes_Bulk_Bwd_Avg_Bytes_Bulk_Matches,
    SUM(CASE WHEN Fwd_Avg_Bytes_Bulk = Bwd_Avg_Packets_Bulk THEN 1 ELSE 0 END) AS Fwd_Avg_Bytes_Bulk_Bwd_Avg_Packets_Bulk_Matches,
    SUM(CASE WHEN Fwd_Avg_Bytes_Bulk = Bwd_Avg_Bulk_Rate THEN 1 ELSE 0 END) AS Fwd_Avg_Bytes_Bulk_Bwd_Avg_Bulk_Rate_Matches,

    SUM(CASE WHEN Fwd_Avg_Packets_Bulk = Fwd_Avg_Bulk_Rate THEN 1 ELSE 0 END) AS Fwd_Avg_Packets_Bulk_Fwd_Avg_Bulk_Rate_Matches,
    SUM(CASE WHEN Fwd_Avg_Packets_Bulk = Bwd_Avg_Bytes_Bulk THEN 1 ELSE 0 END) AS Fwd_Avg_Packets_Bulk_Bwd_Avg_Bytes_Bulk_Matches,
    SUM(CASE WHEN Fwd_Avg_Packets_Bulk = Bwd_Avg_Packets_Bulk THEN 1 ELSE 0 END) AS Fwd_Avg_Packets_Bulk_Bwd_Avg_Packets_Bulk_Matches,
    SUM(CASE WHEN Fwd_Avg_Packets_Bulk = Bwd_Avg_Bulk_Rate THEN 1 ELSE 0 END) AS Fwd_Avg_Packets_Bulk_Bwd_Avg_Bulk_Rate_Matches,

    SUM(CASE WHEN Fwd_Avg_Bulk_Rate = Bwd_Avg_Bytes_Bulk THEN 1 ELSE 0 END) AS Fwd_Avg_Bulk_Rate_Bwd_Avg_Bytes_Bulk_Matches,
    SUM(CASE WHEN Fwd_Avg_Bulk_Rate = Bwd_Avg_Packets_Bulk THEN 1 ELSE 0 END) AS Fwd_Avg_Bulk_Rate_Bwd_Avg_Packets_Bulk_Matches,
    SUM(CASE WHEN Fwd_Avg_Bulk_Rate = Bwd_Avg_Bulk_Rate THEN 1 ELSE 0 END) AS Fwd_Avg_Bulk_Rate_Bwd_Avg_Bulk_Rate_Matches,

    SUM(CASE WHEN Bwd_Avg_Bytes_Bulk = Bwd_Avg_Packets_Bulk THEN 1 ELSE 0 END) AS Bwd_Avg_Bytes_Bulk_Bwd_Avg_Packets_Bulk_Matches,
    SUM(CASE WHEN Bwd_Avg_Bytes_Bulk = Bwd_Avg_Bulk_Rate THEN 1 ELSE 0 END) AS Bwd_Avg_Bytes_Bulk_Bwd_Avg_Bulk_Rate_Matches,
    SUM(CASE WHEN Bwd_Avg_Packets_Bulk = Bwd_Avg_Bulk_Rate THEN 1 ELSE 0 END) AS Bwd_Avg_Packets_Bulk_Bwd_Avg_Bulk_Rate_Matches

FROM [ddos_sampled_db].[dbo].[sampled_500k_dataset];

-- Drop duplicate/redundant columns
ALTER TABLE [ddos_sampled_db].[dbo].[sampled_500k_dataset]
DROP COLUMN
    Subflow_Fwd_Packets,
    Subflow_Bwd_Packets,
    Bwd_URG_Flags,
    Fwd_Header_Length_1,
    Fwd_Avg_Bytes_Bulk,
    Fwd_Avg_Packets_Bulk,
    Fwd_Avg_Bulk_Rate,
    Bwd_Avg_Bytes_Bulk,
    Bwd_Avg_Packets_Bulk,
    Bwd_Avg_Bulk_Rate;