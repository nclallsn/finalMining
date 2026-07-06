-- Remove duplicate rows while keeping the first occurrence
WITH DuplicateRows AS
(
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY
                   [Flow_Duration], [Total_Fwd_Packets], [Total_Backward_Packets], [Total_Length_of_Fwd_Packets],
                   [Total_Length_of_Bwd_Packets], [Fwd_Packet_Length_Max], [Fwd_Packet_Length_Min], [Fwd_Packet_Length_Mean],
                   [Fwd_Packet_Length_Std], [Bwd_Packet_Length_Max], [Bwd_Packet_Length_Min], [Bwd_Packet_Length_Mean],
                   [Bwd_Packet_Length_Std], [Flow_Bytes_s], [Flow_Packets_s], [Flow_IAT_Mean], [Flow_IAT_Std], [Flow_IAT_Max],
                   [Flow_IAT_Min], [Fwd_IAT_Total], [Fwd_IAT_Mean], [Fwd_IAT_Std], [Fwd_IAT_Max], [Fwd_IAT_Min], [Bwd_IAT_Total],
                   [Bwd_IAT_Mean], [Bwd_IAT_Std], [Bwd_IAT_Max], [Bwd_IAT_Min], [Fwd_PSH_Flags], [Bwd_PSH_Flags], [Fwd_URG_Flags],
                   [Bwd_URG_Flags], [Fwd_Header_Length], [Bwd_Header_Length], [Fwd_Packets_s], [Bwd_Packets_s], [Min_Packet_Length],
                   [Max_Packet_Length], [Packet_Length_Mean], [Packet_Length_Std], [Packet_Length_Variance], [FIN_Flag_Count],
                   [SYN_Flag_Count], [RST_Flag_Count], [PSH_Flag_Count], [ACK_Flag_Count], [URG_Flag_Count], [CWE_Flag_Count],
                   [ECE_Flag_Count], [Down_Up_Ratio], [Average_Packet_Size], [Avg_Fwd_Segment_Size], [Avg_Bwd_Segment_Size],
                   [Fwd_Header_Length_1], [Fwd_Avg_Bytes_Bulk], [Fwd_Avg_Packets_Bulk], [Fwd_Avg_Bulk_Rate], [Bwd_Avg_Bytes_Bulk],
                   [Bwd_Avg_Packets_Bulk], [Bwd_Avg_Bulk_Rate], [Subflow_Fwd_Packets], [Subflow_Fwd_Bytes], [Subflow_Bwd_Packets],
                   [Subflow_Bwd_Bytes], [Init_Win_bytes_forward], [Init_Win_bytes_backward], [act_data_pkt_fwd], [min_seg_size_forward],
                   [Active_Mean], [Active_Std], [Active_Max], [Active_Min], [Idle_Mean], [Idle_Std], [Idle_Max], [Idle_Min], [Label]
               ORDER BY (SELECT NULL)
           ) AS rn
    FROM [separate_labels_db].[dbo].[BENIGN]
    --FROM [separate_labels_db].[dbo].[TFTP]
    --FROM [separate_labels_db].[dbo].[UDP]
    --FROM [separate_labels_db].[dbo].[SSDP]
    --FROM [separate_labels_db].[dbo].[NTP]
)
DELETE FROM DuplicateRows
WHERE rn > 1;

-- Drop samples with null values
DELETE FROM dbo.combined
WHERE Flow_Duration IS NULL
   OR Flow_Bytes_s IS NULL
   OR Flow_Packets_s IS NULL
   OR Flow_IAT_Mean IS NULL
   OR Flow_IAT_Max IS NULL
   OR Flow_IAT_Min IS NULL;

-- Column name standardization
-- Prints query that convert column header with capital letters to lower case
SELECT
    'EXEC sp_rename ''[combined_db].[dbo].[combined].['
    + COLUMN_NAME + ']'', '''
    + LOWER(COLUMN_NAME) + ''', ''COLUMN'';' AS rename_command
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'combined'
ORDER BY ORDINAL_POSITION;

-- Removes constant column
DECLARE @sql NVARCHAR(MAX);

SELECT @sql =
    STRING_AGG(
        CAST(
            'IF (SELECT COUNT(DISTINCT [' + name + ']) FROM sampled) <= 1
                ALTER TABLE sampled DROP COLUMN [' + name + '];'
            AS NVARCHAR(MAX)
        ),
        CHAR(13) + CHAR(10)
    )
FROM sys.columns
WHERE object_id = OBJECT_ID('sampled');

EXEC sp_executesql @sql;
