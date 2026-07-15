-- Count total rows
SELECT COUNT(*) AS total_rows
FROM [dbo].[sampled];

-- Count total columns
SELECT COUNT(*) AS total_col
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'sampled'

-- View structure of the table
EXEC sp_help 'sampled';

-- Check for missing values for columns with allowed NULL
SELECT
	SUM(CASE WHEN Flow_Duration IS NULL THEN 1 ELSE 0 END) AS Flow_Duration,
	SUM(CASE WHEN Flow_Bytes_s IS NULL THEN 1 ELSE 0 END) AS Flow_Bytes_s,
	SUM(CASE WHEN Flow_Packets_s IS NULL THEN 1 ELSE 0 END) AS Flow_Packets_s,
	SUM(CASE WHEN Flow_IAT_Mean IS NULL THEN 1 ELSE 0 END) AS Flow_IAT_Mean,
	SUM(CASE WHEN Flow_IAT_Max IS NULL THEN 1 ELSE 0 END) AS Flow_IAT_Max,
	SUM(CASE WHEN Flow_IAT_Min IS NULL THEN 1 ELSE 0 END) AS Flow_IAT_Min
FROM sampled

-- Check for duplicates
SELECT *, COUNT(*) AS duplicate_count
FROM sampled
GROUP BY
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
HAVING COUNT(*) > 1

-- Count distinct values for each column
SELECT
    COUNT(DISTINCT Flow_Duration) AS Flow_Duration,
    COUNT(DISTINCT Total_Fwd_Packets) AS Total_Fwd_Packets,
    COUNT(DISTINCT Total_Backward_Packets) AS Total_Backward_Packets,
    COUNT(DISTINCT Total_Length_of_Fwd_Packets) AS Total_Length_of_Fwd_Packets,
    COUNT(DISTINCT Total_Length_of_Bwd_Packets) AS Total_Length_of_Bwd_Packets,
    COUNT(DISTINCT Fwd_Packet_Length_Max) AS Fwd_Packet_Length_Max,
    COUNT(DISTINCT Fwd_Packet_Length_Min) AS Fwd_Packet_Length_Min,
    COUNT(DISTINCT Fwd_Packet_Length_Mean) AS Fwd_Packet_Length_Mean,
    COUNT(DISTINCT Fwd_Packet_Length_Std) AS Fwd_Packet_Length_Std,
    COUNT(DISTINCT Bwd_Packet_Length_Max) AS Bwd_Packet_Length_Max,
    COUNT(DISTINCT Bwd_Packet_Length_Min) AS Bwd_Packet_Length_Min,
    COUNT(DISTINCT Bwd_Packet_Length_Mean) AS Bwd_Packet_Length_Mean,
    COUNT(DISTINCT Bwd_Packet_Length_Std) AS Bwd_Packet_Length_Std,
    COUNT(DISTINCT Flow_Bytes_s) AS Flow_Bytes_s,
    COUNT(DISTINCT Flow_Packets_s) AS Flow_Packets_s,
    COUNT(DISTINCT Flow_IAT_Mean) AS Flow_IAT_Mean,
    COUNT(DISTINCT Flow_IAT_Std) AS Flow_IAT_Std,
    COUNT(DISTINCT Flow_IAT_Max) AS Flow_IAT_Max,
    COUNT(DISTINCT Flow_IAT_Min) AS Flow_IAT_Min,
    COUNT(DISTINCT Fwd_IAT_Total) AS Fwd_IAT_Total,
    COUNT(DISTINCT Fwd_IAT_Mean) AS Fwd_IAT_Mean,
    COUNT(DISTINCT Fwd_IAT_Std) AS Fwd_IAT_Std,
    COUNT(DISTINCT Fwd_IAT_Max) AS Fwd_IAT_Max,
    COUNT(DISTINCT Fwd_IAT_Min) AS Fwd_IAT_Min,
    COUNT(DISTINCT Bwd_IAT_Total) AS Bwd_IAT_Total,
    COUNT(DISTINCT Bwd_IAT_Mean) AS Bwd_IAT_Mean,
    COUNT(DISTINCT Bwd_IAT_Std) AS Bwd_IAT_Std,
    COUNT(DISTINCT Bwd_IAT_Max) AS Bwd_IAT_Max,
    COUNT(DISTINCT Bwd_IAT_Min) AS Bwd_IAT_Min,
    COUNT(DISTINCT Fwd_PSH_Flags) AS Fwd_PSH_Flags,
    COUNT(DISTINCT Bwd_PSH_Flags) AS Bwd_PSH_Flags,
    COUNT(DISTINCT Fwd_URG_Flags) AS Fwd_URG_Flags,
    COUNT(DISTINCT Bwd_URG_Flags) AS Bwd_URG_Flags,
    COUNT(DISTINCT Fwd_Header_Length) AS Fwd_Header_Length,
    COUNT(DISTINCT Bwd_Header_Length) AS Bwd_Header_Length,
    COUNT(DISTINCT Fwd_Packets_s) AS Fwd_Packets_s,
    COUNT(DISTINCT Bwd_Packets_s) AS Bwd_Packets_s,
    COUNT(DISTINCT Min_Packet_Length) AS Min_Packet_Length,
    COUNT(DISTINCT Max_Packet_Length) AS Max_Packet_Length,
    COUNT(DISTINCT Packet_Length_Mean) AS Packet_Length_Mean,
    COUNT(DISTINCT Packet_Length_Std) AS Packet_Length_Std,
    COUNT(DISTINCT Packet_Length_Variance) AS Packet_Length_Variance,
    COUNT(DISTINCT FIN_Flag_Count) AS FIN_Flag_Count,
    COUNT(DISTINCT SYN_Flag_Count) AS SYN_Flag_Count,
    COUNT(DISTINCT RST_Flag_Count) AS RST_Flag_Count,
    COUNT(DISTINCT PSH_Flag_Count) AS PSH_Flag_Count,
    COUNT(DISTINCT ACK_Flag_Count) AS ACK_Flag_Count,
    COUNT(DISTINCT URG_Flag_Count) AS URG_Flag_Count,
    COUNT(DISTINCT CWE_Flag_Count) AS CWE_Flag_Count,
    COUNT(DISTINCT ECE_Flag_Count) AS ECE_Flag_Count,
    COUNT(DISTINCT Down_Up_Ratio) AS Down_Up_Ratio,
    COUNT(DISTINCT Average_Packet_Size) AS Average_Packet_Size,
    COUNT(DISTINCT Avg_Fwd_Segment_Size) AS Avg_Fwd_Segment_Size,
    COUNT(DISTINCT Avg_Bwd_Segment_Size) AS Avg_Bwd_Segment_Size,
    COUNT(DISTINCT Fwd_Header_Length_1) AS Fwd_Header_Length_1,
    COUNT(DISTINCT Fwd_Avg_Bytes_Bulk) AS Fwd_Avg_Bytes_Bulk,
    COUNT(DISTINCT Fwd_Avg_Packets_Bulk) AS Fwd_Avg_Packets_Bulk,
    COUNT(DISTINCT Fwd_Avg_Bulk_Rate) AS Fwd_Avg_Bulk_Rate,
    COUNT(DISTINCT Bwd_Avg_Bytes_Bulk) AS Bwd_Avg_Bytes_Bulk,
    COUNT(DISTINCT Bwd_Avg_Packets_Bulk) AS Bwd_Avg_Packets_Bulk,
    COUNT(DISTINCT Bwd_Avg_Bulk_Rate) AS Bwd_Avg_Bulk_Rate,
    COUNT(DISTINCT Subflow_Fwd_Packets) AS Subflow_Fwd_Packets,
    COUNT(DISTINCT Subflow_Fwd_Bytes) AS Subflow_Fwd_Bytes,
    COUNT(DISTINCT Subflow_Bwd_Packets) AS Subflow_Bwd_Packets,
    COUNT(DISTINCT Subflow_Bwd_Bytes) AS Subflow_Bwd_Bytes,
    COUNT(DISTINCT Init_Win_bytes_forward) AS Init_Win_bytes_forward,
    COUNT(DISTINCT Init_Win_bytes_backward) AS Init_Win_bytes_backward,
    COUNT(DISTINCT act_data_pkt_fwd) AS act_data_pkt_fwd,
    COUNT(DISTINCT min_seg_size_forward) AS min_seg_size_forward,
    COUNT(DISTINCT Active_Mean) AS Active_Mean,
    COUNT(DISTINCT Active_Std) AS Active_Std,
    COUNT(DISTINCT Active_Max) AS Active_Max,
    COUNT(DISTINCT Active_Min) AS Active_Min,
    COUNT(DISTINCT Idle_Mean) AS Idle_Mean,
    COUNT(DISTINCT Idle_Std) AS Idle_Std,
    COUNT(DISTINCT Idle_Max) AS Idle_Max,
    COUNT(DISTINCT Idle_Min) AS Idle_Min,
    COUNT(DISTINCT Label) AS Label
FROM sampled;

-- Check how many rows does each class have
SELECT 
    label_counts.label,
    label_counts.total_rows
FROM (
    SELECT 
        label,
        COUNT(*) AS total_rows
    FROM [dbo].[sampled_500k_dataset]
    GROUP BY label
) AS label_counts
JOIN (
    SELECT DISTINCT label
    FROM [dbo].[sampled_500k_dataset]
) AS distinct_labels
    ON label_counts.label = distinct_labels.label
ORDER BY label DESC;

