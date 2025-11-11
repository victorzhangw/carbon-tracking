// mock-data.js - 集中管理模擬數據
// 這個檔案統一管理所有模擬數據，方便未來切換到實際API

export const staffList = [
  { id: 1, name: "C220001", department: "離島組", position: "主管" },
  { id: 2, name: "C220002", department: "離島組", position: "資深專員" },
  { id: 3, name: "C230003", department: "原民組", position: "專員" },
  { id: 4, name: "C230004", department: "獨居組", position: "專員" },
  { id: 5, name: "C240005", department: "離島組", position: "專員" },
  { id: 6, name: "C240006", department: "原民組", position: "資深專員" },
  { id: 7, name: "C250007", department: "獨居組", position: "主管" },
  { id: 8, name: "C250008", department: "離島組", position: "專員" },
];

// 通話記錄模擬數據生成函數
export function generateCallRecords(params = {}) {
  const {
    startDate,
    endDate,
    staffId,
    emotionType,
    page = 1,
    pageSize = 10,
  } = params;

  // 設定預設日期範圍
  const defaultEndDate = new Date();
  const defaultStartDate = new Date(
    new Date().setDate(new Date().getDate() - 30)
  );

  const sDate = startDate ? new Date(startDate) : defaultStartDate;
  const eDate = endDate ? new Date(endDate) : defaultEndDate;

  const mockRecords = [];
  const emotions = ["positive", "neutral", "negative"];
  const followupStatuses = ["pending", "inProgress", "completed", "noAction"];
  const totalItems = 183; // 模擬總記錄數

  // 依部門生成不同的情緒分布
  const departmentEmotionDistribution = {
    離島組: { positive: 0.6, neutral: 0.3, negative: 0.1 },
    原民組: { positive: 0.45, neutral: 0.35, negative: 0.2 },
    獨居組: { positive: 0.3, neutral: 0.5, negative: 0.2 },
  };

  for (let i = 1; i <= totalItems; i++) {
    // 隨機生成通話日期（在搜索範圍內）
    const randomDate = new Date(
      sDate.getTime() + Math.random() * (eDate.getTime() - sDate.getTime())
    );

    // 隨機選擇專員
    const randomStaff = staffList[Math.floor(Math.random() * staffList.length)];

    // 如果有專員過濾條件，且不符合則跳過
    if (staffId && parseInt(staffId) !== randomStaff.id) {
      continue;
    }

    // 根據部門權重隨機生成情緒
    const deptDistribution =
      departmentEmotionDistribution[randomStaff.department];
    let mainEmotion;
    const random = Math.random();
    if (random < deptDistribution.positive) {
      mainEmotion = "positive";
    } else if (random < deptDistribution.positive + deptDistribution.neutral) {
      mainEmotion = "neutral";
    } else {
      mainEmotion = "negative";
    }

    // 如果有情緒過濾條件，且不符合則跳過
    if (emotionType && emotionType !== mainEmotion) {
      continue;
    }

    // 生成情緒分析百分比
    let emotionAnalysis = {};
    if (mainEmotion === "positive") {
      emotionAnalysis = {
        positive: 60 + Math.floor(Math.random() * 35),
        neutral: Math.floor(Math.random() * 30),
        negative: 0,
      };
      emotionAnalysis.negative =
        100 - emotionAnalysis.positive - emotionAnalysis.neutral;
    } else if (mainEmotion === "neutral") {
      emotionAnalysis = {
        neutral: 50 + Math.floor(Math.random() * 30),
        positive: Math.floor(Math.random() * 25),
        negative: 0,
      };
      emotionAnalysis.negative =
        100 - emotionAnalysis.positive - emotionAnalysis.neutral;
    } else {
      emotionAnalysis = {
        negative: 55 + Math.floor(Math.random() * 30),
        neutral: Math.floor(Math.random() * 25),
        positive: 0,
      };
      emotionAnalysis.positive =
        100 - emotionAnalysis.negative - emotionAnalysis.neutral;
    }

    // 隨機生成通話時長（2分鐘到30分鐘）
    const duration = Math.floor(Math.random() * 28) + 2;

    // 隨機生成客戶類型
    const customerTypes = ["新客戶", "老客戶", "VIP客戶"];
    const customerType =
      customerTypes[Math.floor(Math.random() * customerTypes.length)];

    // 生成關鍵詞
    const keywordsByEmotion = {
      positive: [
        { word: "感謝", sentiment: "positive" },
        { word: "幫助", sentiment: "positive" },
        { word: "滿意", sentiment: "positive" },
        { word: "很好", sentiment: "positive" },
        { word: "解決", sentiment: "positive" },
      ],
      neutral: [
        { word: "了解", sentiment: "neutral" },
        { word: "考慮", sentiment: "neutral" },
        { word: "可能", sentiment: "neutral" },
        { word: "需要", sentiment: "neutral" },
        { word: "資訊", sentiment: "neutral" },
      ],
      negative: [
        { word: "問題", sentiment: "negative" },
        { word: "不滿", sentiment: "negative" },
        { word: "失望", sentiment: "negative" },
        { word: "投訴", sentiment: "negative" },
        { word: "困擾", sentiment: "negative" },
      ],
    };

    // 根據主要情緒選擇關鍵詞
    const selectedKeywords = [
      ...keywordsByEmotion[mainEmotion]
        .slice(0, 3)
        .map((k) => ({ ...k, count: Math.floor(Math.random() * 5) + 1 })),
    ];

    // 加入少量其他情緒的關鍵詞
    const otherEmotions = emotions.filter((e) => e !== mainEmotion);
    otherEmotions.forEach((emotion) => {
      selectedKeywords.push({
        ...keywordsByEmotion[emotion][
          Math.floor(Math.random() * keywordsByEmotion[emotion].length)
        ],
        count: Math.floor(Math.random() * 3) + 1,
      });
    });

    // 生成摘要
    let summary = "";
    if (mainEmotion === "positive") {
      summary =
        "客戶對於我們的服務表示感謝，對專員的耐心解答感到滿意。通話過程中客戶情緒穩定，並且表示會繼續使用我們的服務。";
    } else if (mainEmotion === "neutral") {
      summary =
        "客戶詢問了關於產品功能的問題，專員提供了詳細說明。客戶表示會考慮我們的建議，但需要一些時間來做決定。";
    } else {
      summary =
        "客戶表達了對服務的不滿，提出了幾個問題點。專員嘗試解釋並提供解決方案，但客戶情緒較為激動。需後續跟進，確保問題得到解決。";
    }

    // 模擬客戶詢問的問題類型
    const questionTypes = [
      "使用感受",
      "話後跟進",
      "資訊查詢",
      "投訴處理",
      "功能建議",
    ];
    const mainQuestion =
      questionTypes[Math.floor(Math.random() * questionTypes.length)];

    // 隨機生成跟進狀態
    const followupStatus =
      followupStatuses[Math.floor(Math.random() * followupStatuses.length)];

    // 模擬跟進成效（解決率）
    let resolutionRate = 0;
    if (followupStatus === "completed") {
      resolutionRate = 0.8 + Math.random() * 0.2; // 80% - 100%
    } else if (followupStatus === "inProgress") {
      resolutionRate = 0.3 + Math.random() * 0.5; // 30% - 80%
    } else if (followupStatus === "pending") {
      resolutionRate = Math.random() * 0.3; // 0% - 30%
    } else {
      resolutionRate = Math.random(); // 對於 noAction，可能是不需要解決，或是已經自行解決
    }

    mockRecords.push({
      id: 1000 + i,
      customerName: `客戶${i}`,
      phoneNumber: `09${Math.floor(10000000 + Math.random() * 90000000)}`,
      callTime: formatDate(randomDate),
      callDate: formatDateOnly(randomDate),
      duration: duration,
      staffId: randomStaff.id,
      staffName: randomStaff.name,
      department: randomStaff.department,
      position: randomStaff.position,
      mainEmotion: mainEmotion,
      emotionAnalysis: emotionAnalysis,
      customerType: customerType,
      mainQuestion: mainQuestion,
      followupStatus: followupStatus,
      resolutionRate: resolutionRate,
      keywords: selectedKeywords,
      summary: summary,
      followupNotes:
        followupStatus !== "pending"
          ? "已與客戶聯繫，說明解決方案，客戶表示接受。"
          : "",
    });
  }

  // 排序記錄（按日期降序）
  mockRecords.sort((a, b) => new Date(b.callTime) - new Date(a.callTime));

  // 分頁處理
  const filteredRecords = mockRecords;
  const start = (page - 1) * pageSize;
  const end = start + pageSize;

  return {
    records: filteredRecords.slice(start, end),
    total: filteredRecords.length,
  };
}

// 獲取統計數據
export function getStatistics(records) {
  const statistics = {
    totalCalls: records.length,
    positiveEmotions: records.filter((r) => r.mainEmotion === "positive")
      .length,
    neutralEmotions: records.filter((r) => r.mainEmotion === "neutral").length,
    negativeEmotions: records.filter((r) => r.mainEmotion === "negative")
      .length,
    averageDuration:
      records.reduce((sum, r) => sum + r.duration, 0) / records.length || 0,
    completedFollowups: records.filter((r) => r.followupStatus === "completed")
      .length,
    pendingFollowups: records.filter((r) => r.followupStatus === "pending")
      .length,
  };

  return statistics;
}

// 獲取按部門分組的情緒統計數據
export function getEmotionStatsByDepartment() {
  const records = generateCallRecords({ pageSize: 1000 }).records;
  return staffList.reduce((acc, staff) => {
    const deptStats = acc[staff.department] || {
      department: staff.department,
      total: 0,
      positive: 0,
      negative: 0,
    };

    records
      .filter((r) => r.department === staff.department)
      .forEach((r) => {
        deptStats.total++;
        if (r.mainEmotion === "positive") deptStats.positive++;
        if (r.mainEmotion === "negative") deptStats.negative++;
      });

    acc[staff.department] = deptStats;
    return acc;
  }, {});
}

// 獲取按日期分組的通話數據
export function getCallsByDate(startDate, endDate) {
  const { records } = generateCallRecords({
    // 明確解構records
    startDate,
    endDate,
    pageSize: 1000,
  });
  // 按日期分組
  const groupedByDate = {};
  records.forEach((record) => {
    const dateKey = record.callDate;
    if (!groupedByDate[dateKey]) {
      groupedByDate[dateKey] = {
        date: dateKey,
        total: 0,
        positive: 0,
        neutral: 0,
        negative: 0,
      };
    }

    groupedByDate[dateKey].total++;
    groupedByDate[dateKey][record.mainEmotion]++;
  });

  // 轉換為陣列並排序
  return Object.values(groupedByDate).sort(
    (a, b) => new Date(a.date) - new Date(b.date)
  );
}

// 獲取按部門分組的統計數據
export function getStatsByDepartment() {
  const records = generateCallRecords({
    pageSize: 1000, // 獲取所有記錄用於統計
  }).records;

  // 按部門分組
  const departments = {};
  records.forEach((record) => {
    const dept = record.department;
    if (!departments[dept]) {
      departments[dept] = {
        department: dept,
        total: 0,
        positive: 0,
        neutral: 0,
        negative: 0,
        completedFollowups: 0,
        averageDuration: 0,
        totalDuration: 0,
      };
    }

    departments[dept].total++;
    departments[dept][record.mainEmotion]++;
    if (record.followupStatus === "completed") {
      departments[dept].completedFollowups++;
    }
    departments[dept].totalDuration += record.duration;
  });

  // 計算平均值
  Object.values(departments).forEach((dept) => {
    dept.averageDuration = dept.totalDuration / dept.total;
    dept.completionRate = dept.completedFollowups / dept.total;
  });

  return Object.values(departments);
}

// 獲取按專員分組的統計數據
export function getStatsByStaff() {
  const records = generateCallRecords({
    pageSize: 1000, // 獲取所有記錄用於統計
  }).records;

  // 按專員分組
  const staffStats = {};
  records.forEach((record) => {
    const staffId = record.staffId;
    if (!staffStats[staffId]) {
      staffStats[staffId] = {
        staffId: staffId,
        staffName: record.staffName,
        department: record.department,
        total: 0,
        positive: 0,
        neutral: 0,
        negative: 0,
        completedFollowups: 0,
        totalDuration: 0,
        satisfactionScore: 0, // 基於正面情緒比例的滿意度評分
      };
    }

    staffStats[staffId].total++;
    staffStats[staffId][record.mainEmotion]++;
    if (record.followupStatus === "completed") {
      staffStats[staffId].completedFollowups++;
    }
    staffStats[staffId].totalDuration += record.duration;
  });

  // 計算統計數據
  Object.values(staffStats).forEach((staff) => {
    staff.averageDuration = staff.totalDuration / staff.total;
    staff.completionRate = staff.completedFollowups / staff.total;
    staff.satisfactionScore =
      (staff.positive * 100 + staff.neutral * 50) / staff.total;
  });

  return Object.values(staffStats);
}

// 獲取每月客戶關懷績效
export function getMonthlyCarePerformance() {
  // 生成過去12個月的模擬數據
  const months = [];
  const currentDate = new Date();

  for (let i = 11; i >= 0; i--) {
    const month = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth() - i,
      1
    );
    const monthName = `${month.getFullYear()}/${month.getMonth() + 1}`;

    months.push({
      month: monthName,
      totalCalls: Math.floor(Math.random() * 500) + 300,
      followupRate: 0.5 + Math.random() * 0.4,
      satisfactionRate: 0.6 + Math.random() * 0.3,
      resolutionRate: 0.7 + Math.random() * 0.25,
    });
  }

  return months;
}

// 依客戶類型獲取統計數據
export function getStatsByCustomerType() {
  const records = generateCallRecords({
    pageSize: 1000, // 獲取所有記錄用於統計
  }).records;

  const customerTypes = {};
  records.forEach((record) => {
    const type = record.customerType;
    if (!customerTypes[type]) {
      customerTypes[type] = {
        type: type,
        total: 0,
        positive: 0,
        neutral: 0,
        negative: 0,
        averageDuration: 0,
        totalDuration: 0,
      };
    }

    customerTypes[type].total++;
    customerTypes[type][record.mainEmotion]++;
    customerTypes[type].totalDuration += record.duration;
  });

  // 計算平均值
  Object.values(customerTypes).forEach((type) => {
    type.averageDuration = type.totalDuration / type.total;
    type.positiveRate = type.positive / type.total;
  });

  return Object.values(customerTypes);
}

// 獲取問題類型統計
export function getQuestionTypeStats() {
  const records = generateCallRecords({
    pageSize: 1000, // 獲取所有記錄用於統計
  }).records;

  const questionTypes = {};
  records.forEach((record) => {
    const type = record.mainQuestion;
    if (!questionTypes[type]) {
      questionTypes[type] = {
        type: type,
        count: 0,
        positive: 0,
        neutral: 0,
        negative: 0,
        resolutionRate: 0,
        totalResolutionRate: 0,
        recordsCount: 0,
      };
    }

    questionTypes[type].count++;
    questionTypes[type][record.mainEmotion]++;
    questionTypes[type].totalResolutionRate += record.resolutionRate;
    questionTypes[type].recordsCount++;
  });

  // 計算平均解決率
  Object.values(questionTypes).forEach((type) => {
    type.resolutionRate = type.totalResolutionRate / type.recordsCount;
  });

  return Object.values(questionTypes);
}

// 日期格式化函數
function formatDate(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  const hour = String(d.getHours()).padStart(2, "0");
  const minute = String(d.getMinutes()).padStart(2, "0");

  return `${year}-${month}-${day} ${hour}:${minute}`;
}

// 僅格式化日期部分
function formatDateOnly(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
}
