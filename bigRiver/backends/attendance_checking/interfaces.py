# 考勤打卡模块:
# 1.	userID check_in（图片）调用 人脸识别模块函数 face_identify，调用
# 假设 check_in_info { info[][2]  第一列是userID，第二列是时间 格式为yy/mm/dd-hh:mm:ss@yy/mm/dd-hh:mm:ss,分别为上班打卡和下班打卡}
# 2.	所有员工打卡信息 view_all_calendar（date）
# 3.	单个员工打卡信息 view_single_calendar（userID,month）
# 4.	bool ask_for_makeup(userID,date)
# 5.	bool ask_for_leave(userID,date)
#
