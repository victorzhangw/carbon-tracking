// AI 廣播劇書庫 - 增強版 JavaScript

// 全域變數
let allBooks = [];
let filteredBooks = [];
let currentPage = 1;
const booksPerPage = 12;
let selectedFiles = [];
let currentView = "card"; // 'card' or 'table'

// 初始化
document.addEventListener("DOMContentLoaded", () => {
  initializeEventListeners();
  loadBooks();
});

// 事件監聽器初始化
function initializeEventListeners() {
  // 搜尋
  const searchInput = document.getElementById("searchInput");
  searchInput.addEventListener("input", debounce(handleSearch, 300));

  // 視圖切換
  document
    .getElementById("cardViewBtn")
    .addEventListener("click", () => switchView("card"));
  document
    .getElementById("tableViewBtn")
    .addEventListener("click", () => switchView("table"));

  // 篩選切換
  const filterToggle = document.getElementById("filterToggle");
  filterToggle.addEventListener("click", toggleFilterPanel);

  // 篩選選項
  document
    .getElementById("timeFilter")
    .addEventListener("change", applyFilters);
  document
    .getElementById("chapterFilter")
    .addEventListener("change", applyFilters);
  document
    .getElementById("sortFilter")
    .addEventListener("change", applyFilters);

  // 分頁
  document
    .getElementById("prevBtn")
    .addEventListener("click", () => changePage(-1));
  document
    .getElementById("nextBtn")
    .addEventListener("click", () => changePage(1));

  // 上傳區域
  const fileInput = document.getElementById("epubFiles");
  const uploadArea = document.getElementById("uploadArea");

  fileInput.addEventListener("change", (e) => {
    addFiles(Array.from(e.target.files));
  });

  uploadArea.addEventListener("click", () => fileInput.click());

  uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = "#2196f3";
    uploadArea.style.background = "#e7f1ff";
  });

  uploadArea.addEventListener("dragleave", () => {
    uploadArea.style.borderColor = "#d8d8d8";
    uploadArea.style.background = "";
  });

  uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = "#d8d8d8";
    uploadArea.style.background = "";
    const files = Array.from(e.dataTransfer.files).filter((f) =>
      f.name.endsWith(".epub")
    );
    addFiles(files);
  });
}

// 視圖切換
function switchView(view) {
  currentView = view;

  // 更新按鈕狀態
  document
    .getElementById("cardViewBtn")
    .classList.toggle("active", view === "card");
  document
    .getElementById("tableViewBtn")
    .classList.toggle("active", view === "table");

  // 重新渲染
  renderBooks();
}

// 載入書籍（優化版 - 後端已包含封面）
async function loadBooks() {
  try {
    const response = await fetch("/api/audiobook/books");
    const result = await response.json();

    if (result.success) {
      allBooks = result.books || [];
      updateStatistics();
      applyFilters();
    } else {
      showEmptyState("載入失敗，請重新整理頁面");
    }
  } catch (error) {
    console.error("載入書籍失敗:", error);
    showEmptyState("載入失敗，請重新整理頁面");
  }
}

// 更新統計資訊
function updateStatistics() {
  const totalBooks = allBooks.length;
  const totalChapters = allBooks.reduce(
    (sum, book) => sum + (book.chapter_count || 0),
    0
  );

  // 計算本週新增
  const oneWeekAgo = new Date();
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
  const weekBooks = allBooks.filter(
    (book) => new Date(book.created_at) > oneWeekAgo
  ).length;

  // 平均章節數
  const avgChapters =
    totalBooks > 0 ? Math.round(totalChapters / totalBooks) : 0;

  document.getElementById("totalBooks").textContent = totalBooks;
  document.getElementById("totalChapters").textContent = totalChapters;
  document.getElementById("weekBooks").textContent = weekBooks;
  document.getElementById("avgChapters").textContent = avgChapters;
}

// 搜尋處理
function handleSearch(e) {
  const searchTerm = e.target.value.toLowerCase().trim();

  if (searchTerm === "") {
    applyFilters();
    return;
  }

  filteredBooks = allBooks.filter((book) =>
    book.title.toLowerCase().includes(searchTerm)
  );

  currentPage = 1;
  renderBooks();
}

// 切換篩選面板
function toggleFilterPanel() {
  const panel = document.getElementById("filterPanel");
  const btn = document.getElementById("filterToggle");

  panel.classList.toggle("active");
  btn.classList.toggle("active");
}

// 應用篩選
function applyFilters() {
  const timeFilter = document.getElementById("timeFilter").value;
  const chapterFilter = document.getElementById("chapterFilter").value;
  const sortFilter = document.getElementById("sortFilter").value;
  const searchTerm = document
    .getElementById("searchInput")
    .value.toLowerCase()
    .trim();

  // 開始篩選
  filteredBooks = [...allBooks];

  // 搜尋篩選
  if (searchTerm) {
    filteredBooks = filteredBooks.filter((book) =>
      book.title.toLowerCase().includes(searchTerm)
    );
  }

  // 時間篩選
  if (timeFilter !== "all") {
    const now = new Date();
    filteredBooks = filteredBooks.filter((book) => {
      const bookDate = new Date(book.created_at);

      switch (timeFilter) {
        case "today":
          return bookDate.toDateString() === now.toDateString();
        case "week":
          const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
          return bookDate >= weekAgo;
        case "month":
          const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
          return bookDate >= monthAgo;
        default:
          return true;
      }
    });
  }

  // 章節數篩選
  if (chapterFilter !== "all") {
    filteredBooks = filteredBooks.filter((book) => {
      const chapters = book.chapter_count || 0;

      switch (chapterFilter) {
        case "short":
          return chapters >= 1 && chapters <= 10;
        case "medium":
          return chapters >= 11 && chapters <= 30;
        case "long":
          return chapters > 30;
        default:
          return true;
      }
    });
  }

  // 排序
  filteredBooks.sort((a, b) => {
    switch (sortFilter) {
      case "newest":
        return new Date(b.created_at) - new Date(a.created_at);
      case "oldest":
        return new Date(a.created_at) - new Date(b.created_at);
      case "chapters_desc":
        return (b.chapter_count || 0) - (a.chapter_count || 0);
      case "chapters_asc":
        return (a.chapter_count || 0) - (b.chapter_count || 0);
      case "title":
        return a.title.localeCompare(b.title, "zh-TW");
      default:
        return 0;
    }
  });

  currentPage = 1;
  renderBooks();
}

// 渲染書籍
function renderBooks() {
  const container = document.getElementById("booksContainer");

  if (filteredBooks.length === 0) {
    showEmptyState("沒有找到符合條件的書籍");
    document.getElementById("pagination").style.display = "none";
    return;
  }

  // 計算分頁
  const totalPages = Math.ceil(filteredBooks.length / booksPerPage);
  const startIndex = (currentPage - 1) * booksPerPage;
  const endIndex = startIndex + booksPerPage;
  const booksToShow = filteredBooks.slice(startIndex, endIndex);

  // 根據視圖類型渲染
  if (currentView === "card") {
    renderCardView(container, booksToShow);
  } else {
    renderTableView(container, booksToShow);
  }

  // 更新分頁
  updatePagination(totalPages);
}

// 渲染卡片視圖
function renderCardView(container, books) {
  const booksHTML = books.map((book) => createBookCard(book)).join("");
  container.innerHTML = `<div class="books-grid">${booksHTML}</div>`;
}

// 渲染表格視圖
function renderTableView(container, books) {
  const rowsHTML = books.map((book) => createTableRow(book)).join("");

  container.innerHTML = `
    <div class="table-view">
      <table>
        <thead>
          <tr>
            <th style="width: 80px;">封面</th>
            <th>書名</th>
            <th style="width: 120px;">章節數</th>
            <th style="width: 150px;">上傳時間</th>
            <th style="width: 200px;">操作</th>
          </tr>
        </thead>
        <tbody>
          ${rowsHTML}
        </tbody>
      </table>
    </div>
  `;
}

// 創建書籍卡片
function createBookCard(book) {
  const date = new Date(book.created_at);
  const dateStr = date.toLocaleDateString("zh-TW", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });

  const coverHTML = book.cover_url
    ? `<img src="${book.cover_url}" alt="${book.title}" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
       <span class="material-icons" style="display: none;">menu_book</span>`
    : `<span class="material-icons">menu_book</span>`;

  return `
    <div class="book-card" onclick="viewChapters('${book.id}')">
      <div class="book-cover">
        ${coverHTML}
      </div>
      <div class="book-info">
        <div class="book-title" title="${book.title}">${book.title}</div>
        <div class="book-meta">
          <div class="book-meta-item">
            <span class="material-icons" style="font-size: 16px;">menu_book</span>
            ${book.chapter_count || 0} 章
          </div>
          <div class="book-meta-item">
            <span class="material-icons" style="font-size: 16px;">calendar_today</span>
            ${dateStr}
          </div>
        </div>
        <div class="book-actions">
          <button class="book-action-btn" onclick="event.stopPropagation(); viewChapters('${
            book.id
          }')" style="width: 100%;">
            <span class="material-icons" style="font-size: 16px;">list</span>
            查看章節
          </button>
        </div>
      </div>
    </div>
  `;
}

// 創建表格行
function createTableRow(book) {
  const date = new Date(book.created_at);
  const dateStr = date.toLocaleDateString("zh-TW", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });

  const coverHTML = book.cover_url
    ? `<img src="${book.cover_url}" alt="${book.title}" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
       <span class="material-icons" style="display: none;">menu_book</span>`
    : `<span class="material-icons">menu_book</span>`;

  return `
    <tr onclick="viewChapters('${book.id}')">
      <td>
        <div class="table-cover">
          ${coverHTML}
        </div>
      </td>
      <td>
        <div class="table-title">
          <strong>${book.title}</strong>
        </div>
      </td>
      <td>${book.chapter_count || 0} 章</td>
      <td>${dateStr}</td>
      <td>
        <button class="book-action-btn" onclick="event.stopPropagation(); viewChapters('${
          book.id
        }')" style="width: 100%;">
          <span class="material-icons" style="font-size: 16px;">list</span>
          查看章節
        </button>
      </td>
    </tr>
  `;
}

// 更新分頁
function updatePagination(totalPages) {
  const pagination = document.getElementById("pagination");
  const pageInfo = document.getElementById("pageInfo");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  if (totalPages <= 1) {
    pagination.style.display = "none";
    return;
  }

  pagination.style.display = "flex";
  pageInfo.textContent = `第 ${currentPage} 頁 / 共 ${totalPages} 頁`;

  prevBtn.disabled = currentPage === 1;
  nextBtn.disabled = currentPage === totalPages;
}

// 換頁
function changePage(direction) {
  const totalPages = Math.ceil(filteredBooks.length / booksPerPage);
  const newPage = currentPage + direction;

  if (newPage >= 1 && newPage <= totalPages) {
    currentPage = newPage;
    renderBooks();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

// 顯示空狀態
function showEmptyState(message) {
  const container = document.getElementById("booksContainer");
  container.innerHTML = `
    <div class="empty-state">
      <span class="material-icons empty-icon" style="font-size: 80px; color: #bdbdbd;">library_books</span>
      <div class="empty-text">${message}</div>
      ${
        allBooks.length === 0
          ? '<button class="upload-btn" onclick="showUploadModal()" style="margin: 0 auto;"><span class="material-icons">upload</span>上傳第一本書</button>'
          : ""
      }
    </div>
  `;
}

// 查看章節（進入 qwen_audiobook_detail 頁面）
function viewChapters(bookId) {
  window.location.href = `/api/audiobook/book/${bookId}/view`;
}

// Modal 控制
function showUploadModal() {
  document.getElementById("uploadModal").classList.add("active");
  selectedFiles = [];
  updateFileList();
}

function closeUploadModal() {
  document.getElementById("uploadModal").classList.remove("active");
  document.getElementById("epubFiles").value = "";
  selectedFiles = [];
  updateFileList();
}

// 檔案處理
function addFiles(files) {
  for (const file of files) {
    if (selectedFiles.length >= 5) {
      showToast("最多只能上傳 5 本書", "warning");
      break;
    }
    if (!selectedFiles.find((f) => f.name === file.name)) {
      selectedFiles.push(file);
    }
  }
  updateFileList();
}

function removeFile(index) {
  selectedFiles.splice(index, 1);
  updateFileList();
}

function updateFileList() {
  const fileList = document.getElementById("fileList");

  if (selectedFiles.length === 0) {
    fileList.innerHTML = "";
    document.getElementById("uploadBtn").disabled = true;
    return;
  }

  document.getElementById("uploadBtn").disabled = false;

  fileList.innerHTML = selectedFiles
    .map(
      (file, index) => `
    <div class="file-item">
      <span style="font-size: 14px; display: flex; align-items: center; gap: 8px;">
        <span class="material-icons" style="font-size: 20px;">description</span>
        ${file.name}
      </span>
      <button 
        style="background: none; border: none; color: #dc3545; cursor: pointer; padding: 0 8px;"
        onclick="removeFile(${index})"
      >
        <span class="material-icons">close</span>
      </button>
    </div>
  `
    )
    .join("");
}

// 上傳處理
async function handleUpload() {
  if (selectedFiles.length === 0) {
    showToast("請選擇檔案", "warning");
    return;
  }

  const uploadBtn = document.getElementById("uploadBtn");
  uploadBtn.disabled = true;
  uploadBtn.textContent = "上傳中...";

  let successCount = 0;
  let failCount = 0;

  for (const file of selectedFiles) {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/api/audiobook/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (result.success) {
        successCount++;
      } else {
        failCount++;
        console.error(`${file.name} 上傳失敗:`, result.error);
      }
    } catch (error) {
      failCount++;
      console.error(`${file.name} 上傳錯誤:`, error);
    }
  }

  uploadBtn.disabled = false;
  uploadBtn.textContent = "開始上傳";

  if (successCount > 0) {
    showToast(`✅ 成功上傳 ${successCount} 本書`);
    await loadBooks();
  }
  if (failCount > 0) {
    showToast(`❌ ${failCount} 本書上傳失敗`, "error");
  }

  closeUploadModal();
}

// Toast 通知
function showToast(message, type = "success") {
  const colors = {
    success: "#4caf50",
    error: "#f44336",
    warning: "#ff9800",
    info: "#2196f3",
  };

  const toast = document.createElement("div");
  toast.style.cssText = `
    position: fixed;
    top: 80px;
    left: 50%;
    transform: translateX(-50%);
    background: ${colors[type] || colors.success};
    color: white;
    padding: 16px 24px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 1001;
    font-size: 15px;
    animation: slideDown 0.3s ease;
  `;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = "slideUp 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// 防抖函數
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// 添加動畫樣式
const style = document.createElement("style");
style.textContent = `
  @keyframes slideDown {
    from {
      transform: translate(-50%, -100%);
      opacity: 0;
    }
    to {
      transform: translate(-50%, 0);
      opacity: 1;
    }
  }

  @keyframes slideUp {
    from {
      transform: translate(-50%, 0);
      opacity: 1;
    }
    to {
      transform: translate(-50%, -100%);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);
