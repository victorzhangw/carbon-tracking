#!/usr/bin/env node
/**
 * 簡單的 Vue 組件語法驗證腳本
 */

const fs = require("fs");
const path = require("path");

function validateVueComponent(filePath) {
  console.log(`🔍 驗證 Vue 組件: ${filePath}`);

  try {
    const content = fs.readFileSync(filePath, "utf8");

    // 檢查基本的 Vue 組件結構
    const hasTemplate = content.includes("<template>");
    const hasScript = content.includes("<script>");
    const hasStyle = content.includes("<style");

    console.log(`✅ 模板區域: ${hasTemplate ? "存在" : "缺失"}`);
    console.log(`✅ 腳本區域: ${hasScript ? "存在" : "缺失"}`);
    console.log(`✅ 樣式區域: ${hasStyle ? "存在" : "缺失"}`);

    // 檢查方法重複
    const methodMatches = content.match(/^\s*(\w+)\s*\(/gm) || [];
    const methodNames = methodMatches.map((match) =>
      match.trim().replace(/\s*\($/, "")
    );
    const duplicates = methodNames.filter(
      (name, index) => methodNames.indexOf(name) !== index
    );

    if (duplicates.length > 0) {
      console.log(`❌ 發現重複的方法: ${[...new Set(duplicates)].join(", ")}`);
      return false;
    } else {
      console.log(`✅ 沒有重複的方法定義`);
    }

    // 檢查情緒相關方法
    const emotionMethods = [
      "getEmotionColor",
      "getEmotionLabel",
      "getEmotionEmoji",
    ];

    console.log("\n📋 情緒相關方法檢查:");
    emotionMethods.forEach((method) => {
      const count = (content.match(new RegExp(`${method}\\s*\\(`, "g")) || [])
        .length;
      const defineCount = (
        content.match(new RegExp(`^\\s*${method}\\s*\\(`, "gm")) || []
      ).length;
      console.log(
        `  ${method}: 定義 ${defineCount} 次, 使用 ${count - defineCount} 次`
      );

      if (defineCount !== 1) {
        console.log(`  ❌ ${method} 應該只定義一次，但發現 ${defineCount} 次`);
        return false;
      }
    });

    console.log("\n🎉 Vue 組件驗證通過！");
    return true;
  } catch (error) {
    console.error(`❌ 驗證失敗: ${error.message}`);
    return false;
  }
}

// 驗證目標組件
const componentPath =
  "webpage/ai-customer-service-frontend/src/components/voice/VoiceInteractionContainer.vue";

if (fs.existsSync(componentPath)) {
  const isValid = validateVueComponent(componentPath);
  process.exit(isValid ? 0 : 1);
} else {
  console.error(`❌ 找不到組件檔案: ${componentPath}`);
  process.exit(1);
}
