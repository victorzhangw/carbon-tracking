<template>
  <div class="import-wizard">
    <Card class="import-card">
      <Steps :current="importStep" class="import-steps">
        <Step
          title="上傳檔案"
          content="請上傳 CSV 或 Excel 格式的關懷對象資料"
        ></Step>
        <Step
          title="欄位對應"
          content="確認資料欄位與系統欄位的對應關係"
        ></Step>
        <Step title="資料驗證" content="檢查資料的有效性並修正問題"></Step>
        <Step title="完成匯入" content="將資料匯入到系統並進行分組"></Step>
      </Steps>

      <!-- 步驟1: 上傳檔案 -->
      <div class="step-content" v-if="importStep === 0">
        <Upload
          type="drag"
          action="#"
          :before-upload="handleFileUpload"
          :max-size="10240"
          accept=".csv, .xlsx, .xls"
          class="file-upload"
        >
          <div class="upload-area">
            <Icon
              type="ios-cloud-upload"
              size="52"
              style="color: #3399ff"
            ></Icon>
            <p>點擊或拖拽文件到此處上傳</p>
            <p class="upload-hint">支持 CSV 和 Excel 格式的文件 (最大 10MB)</p>
          </div>
        </Upload>

        <div
          class="template-download"
          style="margin-top: 20px; text-align: center"
        >
          <Button type="text" icon="md-download" @click="downloadTemplate">
            下載匯入模板
          </Button>
        </div>

        <div v-if="uploadedFile" class="uploaded-file-info">
          <Alert show-icon>
            <template #message>
              <div class="file-info">
                <span>已上傳：{{ uploadedFile.name }}</span>
                <span>大小：{{ formatFileSize(uploadedFile.size) }}</span>
              </div>
            </template>
          </Alert>
          <div class="next-step" style="margin-top: 20px; text-align: right">
            <Button
              type="primary"
              @click="goToNextStep"
              :disabled="!uploadedFile"
            >
              下一步
            </Button>
          </div>
        </div>
      </div>

      <!-- 步驟2: 欄位對應 -->
      <div class="step-content" v-if="importStep === 1">
        <Alert type="warning" show-icon style="margin-bottom: 16px">
          <template #message>
            請確保每個必填欄位都有對應的匯入資料欄位，以確保資料能夠正確導入系統。
          </template>
        </Alert>

        <div class="preview-table">
          <p class="preview-title">文件預覽（前 5 筆資料）：</p>
          <Table
            :columns="previewColumns"
            :data="previewData"
            size="small"
            border
            class="data-preview-table"
          ></Table>
        </div>

        <Divider>欄位對應</Divider>

        <Form :model="mappingForm" :label-width="120">
          <FormItem label="姓名" required>
            <Select v-model="mappingForm.name" style="width: 200px">
              <Option value="">請選擇</Option>
              <Option
                v-for="(column, index) in fileColumns"
                :key="index"
                :value="column"
              >
                {{ column }}
              </Option>
            </Select>
            <span class="field-required">(必填)</span>
          </FormItem>
          <FormItem label="聯絡電話" required>
            <Select v-model="mappingForm.phone" style="width: 200px">
              <Option value="">請選擇</Option>
              <Option
                v-for="(column, index) in fileColumns"
                :key="index"
                :value="column"
              >
                {{ column }}
              </Option>
            </Select>
            <span class="field-required">(必填)</span>
          </FormItem>
          <FormItem label="年齡">
            <Select v-model="mappingForm.age" style="width: 200px">
              <Option value="">請選擇</Option>
              <Option
                v-for="(column, index) in fileColumns"
                :key="index"
                :value="column"
              >
                {{ column }}
              </Option>
            </Select>
          </FormItem>
          <FormItem label="性別">
            <Select v-model="mappingForm.gender" style="width: 200px">
              <Option value="">請選擇</Option>
              <Option
                v-for="(column, index) in fileColumns"
                :key="index"
                :value="column"
              >
                {{ column }}
              </Option>
            </Select>
          </FormItem>
          <FormItem label="地址">
            <Select v-model="mappingForm.address" style="width: 200px">
              <Option value="">請選擇</Option>
              <Option
                v-for="(column, index) in fileColumns"
                :key="index"
                :value="column"
              >
                {{ column }}
              </Option>
            </Select>
          </FormItem>
          <FormItem label="備註">
            <Select v-model="mappingForm.notes" style="width: 200px">
              <Option value="">請選擇</Option>
              <Option
                v-for="(column, index) in fileColumns"
                :key="index"
                :value="column"
              >
                {{ column }}
              </Option>
            </Select>
          </FormItem>
        </Form>

        <div class="step-actions">
          <Button @click="importStep = 0">上一步</Button>
          <Button
            type="primary"
            @click="validateMapping"
            :disabled="!isValidMapping"
            style="margin-left: 8px"
          >
            下一步
          </Button>
        </div>
      </div>

      <!-- 步驟3: 資料驗證 -->
      <div class="step-content" v-if="importStep === 2">
        <Alert type="info" show-icon style="margin-bottom: 16px">
          <template #message>
            系統已對資料進行初步驗證，請檢查並修正下列問題。
          </template>
        </Alert>

        <div class="validation-summary">
          <Card class="validation-card">
            <div class="validation-info">
              <div class="validation-item">
                <div class="validation-label">總資料數</div>
                <div class="validation-value">{{ validationStats.total }}</div>
              </div>
              <div class="validation-item">
                <div class="validation-label">有效資料</div>
                <div class="validation-value success">
                  {{ validationStats.valid }}
                </div>
              </div>
              <div class="validation-item">
                <div class="validation-label">警告資料</div>
                <div class="validation-value warning">
                  {{ validationStats.warning }}
                </div>
              </div>
              <div class="validation-item">
                <div class="validation-label">錯誤資料</div>
                <div class="validation-value error">
                  {{ validationStats.error }}
                </div>
              </div>
            </div>
          </Card>
        </div>

        <Tabs v-model="validationTab" class="validation-tabs">
          <TabPane label="全部資料" name="all">
            <Table
              :columns="validationColumns"
              :data="validatedData"
              size="small"
              border
              height="300"
            >
              <template #status="{ row }">
                <Badge
                  :status="getValidationStatus(row.validationStatus)"
                  :text="getValidationText(row.validationStatus)"
                />
              </template>
              <template #issues="{ row }">
                <ul class="issue-list" v-if="row.issues && row.issues.length">
                  <li
                    v-for="(issue, idx) in row.issues"
                    :key="idx"
                    :class="issue.type"
                  >
                    {{ issue.message }}
                  </li>
                </ul>
                <span v-else>無問題</span>
              </template>
              <template #action="{ index }">
                <Button
                  type="primary"
                  size="small"
                  @click="editValidatedRow(index)"
                >
                  修正
                </Button>
                <Button
                  type="error"
                  size="small"
                  @click="removeValidatedRow(index)"
                  style="margin-left: 5px"
                >
                  移除
                </Button>
              </template>
            </Table>
          </TabPane>
          <TabPane
            label="有問題的資料"
            name="issues"
            :disabled="validationStats.warning + validationStats.error === 0"
          >
            <Table
              :columns="validationColumns"
              :data="validatedDataWithIssues"
              size="small"
              border
              height="300"
            >
              <template #status="{ row }">
                <Badge
                  :status="getValidationStatus(row.validationStatus)"
                  :text="getValidationText(row.validationStatus)"
                />
              </template>
              <template #issues="{ row }">
                <ul class="issue-list" v-if="row.issues && row.issues.length">
                  <li
                    v-for="(issue, idx) in row.issues"
                    :key="idx"
                    :class="issue.type"
                  >
                    {{ issue.message }}
                  </li>
                </ul>
              </template>
              <template #action="{ index }">
                <Button
                  type="primary"
                  size="small"
                  @click="editValidatedRow(getOriginalIndex(index, 'issues'))"
                >
                  修正
                </Button>
                <Button
                  type="error"
                  size="small"
                  @click="removeValidatedRow(getOriginalIndex(index, 'issues'))"
                  style="margin-left: 5px"
                >
                  移除
                </Button>
              </template>
            </Table>
          </TabPane>
        </Tabs>

        <div class="import-options" style="margin-top: 20px">
          <Form :model="importOptions" inline>
            <FormItem label="匯入後分組">
              <Select v-model="importOptions.groupId" style="width: 200px">
                <Option value="">不分組</Option>
                <Option
                  v-for="group in groupList"
                  :value="group.id"
                  :key="group.id"
                >
                  {{ group.name }}
                </Option>
              </Select>
            </FormItem>
            <FormItem>
              <Button
                type="primary"
                @click="showCreateGroupModal"
                icon="md-add"
                size="small"
              >
                新增組別
              </Button>
            </FormItem>
          </Form>
        </div>

        <div class="data-handling-options">
          <Checkbox v-model="importOptions.skipErrors"
            >忽略錯誤資料，僅匯入有效資料</Checkbox
          >
          <Checkbox v-model="importOptions.overwriteDuplicates"
            >覆蓋已存在的重複資料（依電話號碼比對）</Checkbox
          >
        </div>

        <div class="step-actions">
          <Button @click="importStep = 1">上一步</Button>
          <Button
            type="primary"
            @click="finalizeImport"
            :disabled="validationStats.error > 0 && !importOptions.skipErrors"
            style="margin-left: 8px"
          >
            開始匯入
          </Button>
        </div>
      </div>

      <!-- 步驟4: 完成匯入 -->
      <div class="step-content" v-if="importStep === 3">
        <div class="import-result" v-if="importResult.status">
          <div class="result-icon">
            <Icon
              :type="
                importResult.status === 'success'
                  ? 'md-checkmark-circle'
                  : 'md-close-circle'
              "
              :size="60"
              :class="importResult.status"
            ></Icon>
          </div>
          <div class="result-message">
            <h3>{{ importResult.title }}</h3>
            <p>{{ importResult.message }}</p>
          </div>

          <Divider>匯入結果統計</Divider>

          <Row :gutter="16" class="import-stats">
            <Col span="6">
              <Card class="stat-card total">
                <div class="stat-content">
                  <div class="stat-value">{{ importResult.stats.total }}</div>
                  <div class="stat-label">總計資料</div>
                </div>
              </Card>
            </Col>
            <Col span="6">
              <Card class="stat-card imported">
                <div class="stat-content">
                  <div class="stat-value">
                    {{ importResult.stats.imported }}
                  </div>
                  <div class="stat-label">成功匯入</div>
                </div>
              </Card>
            </Col>
            <Col span="6">
              <Card class="stat-card updated">
                <div class="stat-content">
                  <div class="stat-value">{{ importResult.stats.updated }}</div>
                  <div class="stat-label">更新資料</div>
                </div>
              </Card>
            </Col>
            <Col span="6">
              <Card class="stat-card failed">
                <div class="stat-content">
                  <div class="stat-value">{{ importResult.stats.failed }}</div>
                  <div class="stat-label">匯入失敗</div>
                </div>
              </Card>
            </Col>
          </Row>

          <div
            class="import-actions"
            style="margin-top: 30px; text-align: center"
          >
            <Button
              type="primary"
              @click="completeImport"
              icon="md-list"
              style="margin-right: 10px"
            >
              查看關懷對象列表
            </Button>
            <Button @click="resetImport" icon="md-refresh"> 重新匯入 </Button>
          </div>

          <div class="error-log" v-if="importResult.errorLog.length > 0">
            <Divider>匯入錯誤日誌</Divider>
            <Table
              :columns="errorLogColumns"
              :data="importResult.errorLog"
              size="small"
              border
              max-height="200"
            ></Table>
            <div style="margin-top: 10px">
              <Button
                type="primary"
                ghost
                icon="md-download"
                size="small"
                @click="downloadErrorLog"
              >
                下載錯誤日誌
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Card>

    <!-- 新增組別 Modal -->
    <Modal
      v-model="createGroupModal.visible"
      title="新增組別"
      :mask-closable="false"
      width="500"
    >
      <Form :model="createGroupModal.form" :label-width="80">
        <FormItem label="組別名稱" required>
          <Input
            v-model="createGroupModal.form.name"
            placeholder="請輸入組別名稱"
          />
        </FormItem>
        <FormItem label="描述">
          <Input
            v-model="createGroupModal.form.description"
            type="textarea"
            :rows="3"
            placeholder="請輸入組別描述"
          />
        </FormItem>
      </Form>
      <template #footer>
        <Button @click="createGroupModal.visible = false">取消</Button>
        <Button
          type="primary"
          @click="quickCreateGroup"
          :loading="createGroupModal.saving"
          >確定</Button
        >
      </template>
    </Modal>

    <!-- 修正資料 Modal -->
    <Modal
      v-model="editDataModal.visible"
      title="修正資料"
      :mask-closable="false"
      width="650"
    >
      <Form
        :model="editDataModal.form"
        :label-width="100"
        v-if="editDataModal.form"
      >
        <FormItem
          label="姓名"
          required
          :class="{ 'error-field': editDataModal.errors.name }"
        >
          <Input v-model="editDataModal.form.name" />
          <div class="error-message" v-if="editDataModal.errors.name">
            {{ editDataModal.errors.name }}
          </div>
        </FormItem>
        <FormItem
          label="聯絡電話"
          required
          :class="{ 'error-field': editDataModal.errors.phone }"
        >
          <Input v-model="editDataModal.form.phone" />
          <div class="error-message" v-if="editDataModal.errors.phone">
            {{ editDataModal.errors.phone }}
          </div>
        </FormItem>
        <FormItem
          label="年齡"
          :class="{ 'error-field': editDataModal.errors.age }"
        >
          <InputNumber
            v-model="editDataModal.form.age"
            :min="0"
            :max="150"
            style="width: 100%"
          />
          <div class="error-message" v-if="editDataModal.errors.age">
            {{ editDataModal.errors.age }}
          </div>
        </FormItem>
        <FormItem label="性別">
          <RadioGroup v-model="editDataModal.form.gender">
            <Radio label="male">男</Radio>
            <Radio label="female">女</Radio>
            <Radio label="other">其他</Radio>
          </RadioGroup>
        </FormItem>
        <FormItem label="地址">
          <Input v-model="editDataModal.form.address" />
        </FormItem>
        <FormItem label="備註">
          <Input type="textarea" v-model="editDataModal.form.notes" :rows="3" />
        </FormItem>
      </Form>
      <template #footer>
        <Button @click="editDataModal.visible = false">取消</Button>
        <Button
          type="primary"
          @click="saveEditedData"
          :loading="editDataModal.saving"
          >確定</Button
        >
      </template>
    </Modal>
  </div>
</template>
<script>
export default {
  name: "ImportWizard",
  props: {
    groupList: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      importStep: 0,
      uploadedFile: null,
      fileColumns: [],
      previewData: [],
      previewColumns: [],
      validationTab: "all",
      validatedData: [],
      validationColumns: [
        {
          title: "#",
          type: "index",
          width: 60,
        },
        {
          title: "姓名",
          key: "name",
          minWidth: 100,
        },
        {
          title: "聯絡電話",
          key: "phone",
          width: 120,
        },
        {
          title: "年齡",
          key: "age",
          width: 80,
        },
        {
          title: "性別",
          key: "gender",
          width: 80,
        },
        {
          title: "狀態",
          slot: "status",
          width: 100,
        },
        {
          title: "問題",
          slot: "issues",
          minWidth: 200,
        },
        {
          title: "操作",
          slot: "action",
          width: 130,
          align: "center",
        },
      ],
      validationStats: {
        total: 0,
        valid: 0,
        warning: 0,
        error: 0,
      },
      mappingForm: {
        name: "",
        phone: "",
        age: "",
        gender: "",
        address: "",
        notes: "",
      },
      importOptions: {
        groupId: "",
        skipErrors: true,
        overwriteDuplicates: false,
      },
      importResult: {
        status: "",
        title: "",
        message: "",
        stats: {
          total: 0,
          imported: 0,
          updated: 0,
          failed: 0,
        },
        errorLog: [],
      },
      errorLogColumns: [
        {
          title: "行號",
          key: "row",
          width: 80,
        },
        {
          title: "姓名",
          key: "name",
          minWidth: 100,
        },
        {
          title: "聯絡電話",
          key: "phone",
          width: 120,
        },
        {
          title: "錯誤原因",
          key: "reason",
          minWidth: 200,
        },
      ],

      // 新增組別 Modal
      createGroupModal: {
        visible: false,
        saving: false,
        form: {
          name: "",
          description: "",
        },
      },

      // 修正數據 Modal
      editDataModal: {
        visible: false,
        rowIndex: -1,
        form: null,
        errors: {},
        saving: false,
      },
    };
  },

  computed: {
    // 計算是否有有效的欄位對應
    isValidMapping() {
      return !!this.mappingForm.name && !!this.mappingForm.phone;
    },

    // 過濾出僅有問題的數據
    validatedDataWithIssues() {
      return this.validatedData.filter(
        (item) =>
          item.validationStatus === "warning" ||
          item.validationStatus === "error"
      );
    },
  },

  methods: {
    // 處理檔案上傳
    handleFileUpload(file) {
      // 檢查檔案大小
      if (file.size > 10 * 1024 * 1024) {
        this.$Message.error("檔案大小不能超過 10MB");
        return false;
      }

      // 檢查檔案類型
      const types = ["csv", "xlsx", "xls"];
      const extension = file.name.split(".").pop().toLowerCase();

      if (!types.includes(extension)) {
        this.$Message.error("僅支持 CSV 和 Excel 格式的文件");
        return false;
      }

      // 設置上傳的檔案
      this.uploadedFile = file;

      // 模擬解析檔案
      this.simulateFileParser(file);

      // 阻止自動上傳
      return false;
    },

    // 模擬檔案解析
    simulateFileParser(file) {
      // 模擬解析 CSV/Excel 文件的過程
      console.log('解析檔案:', file.name)
      setTimeout(() => {
        // 模擬檔案欄位
        this.fileColumns = ["姓名", "電話", "年齡", "性別", "地址", "備註"];

        // 模擬預覽數據
        this.previewData = [
          {
            姓名: "陳○○",
            電話: "0912XX5678",
            年齡: "65",
            性別: "男",
            地址: "台北市松山區松山路123號",
            備註: "定期關懷對象",
          },
          {
            姓名: "王○○",
            電話: "0923XX6789",
            年齡: "72",
            性別: "女",
            地址: "新北市板橋區板橋路456號",
            備註: "需要特別關懷",
          },
          {
            姓名: "呂○○",
            電話: "0934XX7890",
            年齡: "80",
            性別: "女",
            地址: "台北市信義區信義路789號",
            備註: "行動不便",
          },
          {
            姓名: "李○○",
            電話: "0945XX8901",
            年齡: "68",
            性別: "男",
            地址: "新北市中和區中和路101號",
            備註: "獨居老人",
          },
          {
            姓名: "張○○",
            電話: "0956XX9012",
            年齡: "85",
            性別: "女",
            地址: "台北市文山區文山路202號",
            備註: "慢性病患者",
          },
        ];

        // 生成預覽表格的列定義
        this.previewColumns = this.fileColumns.map((col) => ({
          title: col,
          key: col,
          width: col === "地址" || col === "備註" ? 200 : 100,
        }));

        // 自動設置欄位對應
        this.mappingForm = {
          name: "姓名",
          phone: "電話",
          age: "年齡",
          gender: "性別",
          address: "地址",
          notes: "備註",
        };
      }, 1000);
    },

    // 轉到下一步
    goToNextStep() {
      this.importStep++;
    },

    // 驗證欄位對應
    validateMapping() {
      if (!this.mappingForm.name || !this.mappingForm.phone) {
        this.$Message.error("請至少設置姓名和聯絡電話的欄位對應");
        return;
      }

      this.importStep = 2;

      // 模擬數據驗證過程
      setTimeout(() => {
        // 生成驗證數據（從預覽數據生成，加入驗證狀態）
        this.validatedData = [];

        // 模擬更多數據
        const totalData = [...this.previewData];

        // 添加一些有問題的數據
        totalData.push(
          {
            姓名: "黃小姐",
            電話: "",
            年齡: "45",
            性別: "女",
            地址: "台中市西區西區路789號",
            備註: "聯絡電話缺失",
          },
          {
            姓名: "",
            電話: "0978123456",
            年齡: "60",
            性別: "男",
            地址: "高雄市前鎮區前鎮路123號",
            備註: "姓名缺失",
          },
          {
            姓名: "鄭先生",
            電話: "09123",
            年齡: "不詳",
            性別: "男",
            地址: "台南市東區東區路456號",
            備註: "電話號碼不完整",
          },
          {
            姓名: "劉女士",
            電話: "0912345678",
            年齡: "200",
            性別: "女",
            地址: "屏東市屏東路789號",
            備註: "年齡值不合理",
          }
        );

        // 驗證數據並轉換為系統格式
        totalData.forEach((item) => {
          const validatedItem = {
            name: item[this.mappingForm.name] || "",
            phone: item[this.mappingForm.phone] || "",
            age: this.mappingForm.age
              ? parseInt(item[this.mappingForm.age]) || null
              : null,
            gender: this.mappingForm.gender
              ? this.mapGender(item[this.mappingForm.gender])
              : null,
            address: this.mappingForm.address
              ? item[this.mappingForm.address]
              : "",
            notes: this.mappingForm.notes ? item[this.mappingForm.notes] : "",
            issues: [],
            validationStatus: "valid", // 默認為有效
          };

          // 驗證並添加問題
          if (!validatedItem.name) {
            validatedItem.issues.push({
              type: "error",
              message: "姓名不能為空",
            });
            validatedItem.validationStatus = "error";
          }

          if (!validatedItem.phone) {
            validatedItem.issues.push({
              type: "error",
              message: "聯絡電話不能為空",
            });
            validatedItem.validationStatus = "error";
          } else if (!/^09\d{8}$/.test(validatedItem.phone)) {
            validatedItem.issues.push({
              type: "error",
              message: "聯絡電話格式不正確，應為09開頭的10位數字",
            });
            validatedItem.validationStatus = "error";
          }

          if (validatedItem.age !== null) {
            if (validatedItem.age < 0 || validatedItem.age > 150) {
              validatedItem.issues.push({
                type: "warning",
                message: "年齡值不合理，應在0-150之間",
              });
              validatedItem.validationStatus =
                validatedItem.validationStatus === "error"
                  ? "error"
                  : "warning";
            }
          }

          this.validatedData.push(validatedItem);
        });

        // 計算統計數據
        this.calculateValidationStats();
      }, 1200);
    },

    // 計算驗證統計數據
    calculateValidationStats() {
      const total = this.validatedData.length;
      const valid = this.validatedData.filter(
        (item) => item.validationStatus === "valid"
      ).length;
      const warning = this.validatedData.filter(
        (item) => item.validationStatus === "warning"
      ).length;
      const error = this.validatedData.filter(
        (item) => item.validationStatus === "error"
      ).length;

      this.validationStats = { total, valid, warning, error };
    },

    // 映射性別值
    mapGender(value) {
      const lowerValue = String(value).toLowerCase();
      if (["男", "male", "m", "先生"].includes(lowerValue)) {
        return "male";
      } else if (["女", "female", "f", "小姐", "女士"].includes(lowerValue)) {
        return "female";
      }
      return "other";
    },

    // 獲取驗證狀態樣式
    getValidationStatus(status) {
      const statusMap = {
        valid: "success",
        warning: "warning",
        error: "error",
      };
      return statusMap[status] || "default";
    },

    // 獲取驗證狀態文字
    getValidationText(status) {
      const textMap = {
        valid: "有效",
        warning: "警告",
        error: "錯誤",
      };
      return textMap[status] || "未知";
    },

    // 編輯驗證行
    editValidatedRow(index) {
      this.editDataModal.rowIndex = index;
      this.editDataModal.form = { ...this.validatedData[index] };
      this.editDataModal.errors = {};
      this.editDataModal.visible = true;
    },

    // 移除驗證行
    removeValidatedRow(index) {
      this.$Modal.confirm({
        title: "確認移除",
        content: "確定要從匯入數據中移除此筆資料嗎？",
        onOk: () => {
          this.validatedData.splice(index, 1);
          this.calculateValidationStats();
        },
      });
    },

    // 保存編輯過的數據
    saveEditedData() {
      // 驗證表單
      const errors = {};

      if (!this.editDataModal.form.name) {
        errors.name = "姓名不能為空";
      }

      if (!this.editDataModal.form.phone) {
        errors.phone = "聯絡電話不能為空";
      } else if (!/^09\d{8}$/.test(this.editDataModal.form.phone)) {
        errors.phone = "聯絡電話格式不正確，應為09開頭的10位數字";
      }

      if (
        this.editDataModal.form.age !== null &&
        (this.editDataModal.form.age < 0 || this.editDataModal.form.age > 150)
      ) {
        errors.age = "年齡值不合理，應在0-150之間";
      }

      // 如果有錯誤，顯示錯誤並返回
      if (Object.keys(errors).length > 0) {
        this.editDataModal.errors = errors;
        return;
      }

      // 更新數據
      this.editDataModal.saving = true;

      setTimeout(() => {
        // 更新驗證狀態
        const issues = [];
        let validationStatus = "valid";

        // 重新驗證（主要針對警告類型的驗證）
        if (
          this.editDataModal.form.age !== null &&
          (this.editDataModal.form.age < 0 || this.editDataModal.form.age > 150)
        ) {
          issues.push({
            type: "warning",
            message: "年齡值不合理，應在0-150之間",
          });
          validationStatus = "warning";
        }

        // 更新數據
        this.validatedData[this.editDataModal.rowIndex] = {
          ...this.editDataModal.form,
          issues,
          validationStatus,
        };

        // 重新計算統計數據
        this.calculateValidationStats();

        this.editDataModal.saving = false;
        this.editDataModal.visible = false;

        this.$Message.success("數據已修正");
      }, 500);
    },

    // 獲取原始索引（用於從問題視圖中獲取完整數據視圖中的索引）
    getOriginalIndex(index, view) {
      if (view === "issues") {
        const issuesData = this.validatedDataWithIssues;
        const item = issuesData[index];
        return this.validatedData.findIndex(
          (data) => data.name === item.name && data.phone === item.phone
        );
      }
      return index;
    },

    // 顯示創建組別模態框
    showCreateGroupModal() {
      this.createGroupModal.form = {
        name: "",
        description: "",
      };
      this.createGroupModal.visible = true;
    },

    // 快速創建組別
    quickCreateGroup() {
      if (!this.createGroupModal.form.name.trim()) {
        this.$Message.error("請輸入組別名稱");
        return;
      }

      this.createGroupModal.saving = true;

      // 模擬API操作
      setTimeout(() => {
        // 觸發父組件事件
        const newGroup = {
          id: `new-${Date.now()}`,
          name: this.createGroupModal.form.name,
          description: this.createGroupModal.form.description,
          count: 0,
          createdAt: new Date().toISOString().split("T")[0],
        };

        this.$emit("create-group", newGroup);

        // 選擇新創建的組別
        this.importOptions.groupId = newGroup.id;

        this.$Message.success("組別創建成功！");
        this.createGroupModal.saving = false;
        this.createGroupModal.visible = false;
      }, 500);
    },

    // 完成匯入準備，進行最終匯入
    finalizeImport() {
      // 如果有錯誤且未選擇忽略錯誤，則提示用戶
      if (this.validationStats.error > 0 && !this.importOptions.skipErrors) {
        this.$Modal.confirm({
          title: "資料有誤",
          content: `資料中存在 ${this.validationStats.error} 個錯誤，確定要繼續匯入嗎？建議先修正錯誤。`,
          onOk: () => {
            this.processImport();
          },
        });
      } else {
        this.processImport();
      }
    },

    // 處理匯入過程
    processImport() {
      this.importStep = 3;

      // 模擬匯入過程
      setTimeout(() => {
        const validData = this.importOptions.skipErrors
          ? this.validatedData.filter(
              (item) => item.validationStatus !== "error"
            )
          : this.validatedData;

        // 模擬API響應
        const total = validData.length;
        const failed = Math.floor(Math.random() * 3); // 0-2個失敗
        const updated = Math.floor(Math.random() * 5); // 0-4個更新
        const imported = total - failed - updated;

        // 生成錯誤日誌
        const errorLog = [];
        if (failed > 0) {
          for (let i = 0; i < failed; i++) {
            errorLog.push({
              row: Math.floor(Math.random() * 100) + 1,
              name: ["C220001", "C220002", "C230003"][
                Math.floor(Math.random() * 3)
              ],
              phone: "09" + Math.floor(Math.random() * 100000000),
              reason: ["資料格式不正確", "電話號碼已存在", "系統錯誤"][
                Math.floor(Math.random() * 3)
              ],
            });
          }
        }

        // 設置匯入結果
        this.importResult = {
          status: failed < total ? "success" : "error",
          title: failed < total ? "匯入成功" : "匯入失敗",
          message:
            failed < total
              ? `成功匯入 ${imported} 筆資料，更新 ${updated} 筆資料，失敗 ${failed} 筆資料。`
              : "所有資料均匯入失敗，請檢查資料格式或聯繫系統管理員。",
          stats: {
            total,
            imported,
            updated,
            failed,
          },
          errorLog,
        };
      }, 2000);
    },

    // 完成匯入，回到列表頁
    completeImport() {
      this.$emit("complete-import");
      this.resetImportState();
    },

    // 重新開始匯入
    resetImport() {
      this.resetImportState();
      this.importStep = 0;
    },

    // 重置匯入狀態
    resetImportState() {
      this.uploadedFile = null;
      this.fileColumns = [];
      this.previewData = [];
      this.previewColumns = [];
      this.validatedData = [];
      this.validationStats = {
        total: 0,
        valid: 0,
        warning: 0,
        error: 0,
      };
      this.mappingForm = {
        name: "",
        phone: "",
        age: "",
        gender: "",
        address: "",
        notes: "",
      };
      this.importOptions = {
        groupId: "",
        skipErrors: true,
        overwriteDuplicates: false,
      };
    },

    // 下載模板
    downloadTemplate() {
      // 模擬下載模板動作
      const link = document.createElement("a");
      link.href = "#";
      link.setAttribute("download", "關懷對象匯入模板.xlsx");
      link.click();

      this.$Message.success("模板下載已開始");
    },

    // 下載錯誤日誌
    downloadErrorLog() {
      if (this.importResult.errorLog.length === 0) return;

      // 模擬下載文件
      const link = document.createElement("a");
      link.href = "#";
      link.setAttribute("download", "匯入錯誤日誌.csv");
      link.click();

      this.$Message.success("錯誤日誌下載已開始");
    },

    // 格式化文件大小
    formatFileSize(bytes) {
      if (bytes === 0) return "0 B";

      const k = 1024;
      const sizes = ["B", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));

      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    },
  },
};
</script>
<style scoped>
/* 匯入功能樣式 */
.import-card {
  margin-top: 0;
}

.import-steps {
  margin-bottom: 30px;
}

.step-content {
  margin-top: 20px;
}

.file-upload {
  width: 100%;
}

.upload-area {
  padding: 40px 0;
  text-align: center;
}

.upload-hint {
  color: #808695;
  font-size: 12px;
  margin-top: 8px;
}

.uploaded-file-info {
  margin-top: 20px;
}

.file-info {
  display: flex;
  justify-content: space-between;
}

.preview-table {
  margin-top: 16px;
  margin-bottom: 24px;
}

.preview-title {
  margin-bottom: 8px;
  font-weight: 500;
}

.field-required {
  color: #ed4014;
  margin-left: 8px;
}

.step-actions {
  margin-top: 30px;
  text-align: right;
}

.validation-summary {
  margin-bottom: 20px;
}

.validation-card {
  background-color: #f8f8f9;
}

.validation-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.validation-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  flex: 1;
}

.validation-label {
  font-size: 14px;
  color: #515a6e;
  margin-bottom: 8px;
}

.validation-value {
  font-size: 24px;
  font-weight: bold;
  color: #2d8cf0;
}

.validation-value.success {
  color: #19be6b;
}

.validation-value.warning {
  color: #ff9900;
}

.validation-value.error {
  color: #ed4014;
}

.validation-tabs {
  margin-bottom: 16px;
}

.issue-list {
  margin: 0;
  padding-left: 18px;
  font-size: 12px;
}

.issue-list li {
  margin-bottom: 4px;
}

.issue-list li.error {
  color: #ed4014;
}

.issue-list li.warning {
  color: #ff9900;
}

.import-options {
  background-color: #f8f8f9;
  padding: 16px;
  border-radius: 6px;
  margin-bottom: 16px;
}

.data-handling-options {
  margin-bottom: 20px;
}

.error-field input,
.error-field .ivu-input-number {
  border-color: #ed4014;
}

.error-message {
  font-size: 12px;
  color: #ed4014;
  margin-top: 4px;
}

/* 匯入結果樣式 */
.import-result {
  text-align: center;
  padding: 20px 0;
}

.result-icon {
  margin-bottom: 20px;
}

.result-icon .success {
  color: #19be6b;
}

.result-icon .error {
  color: #ed4014;
}

.result-message h3 {
  margin-bottom: 10px;
  font-size: 20px;
}

.import-stats {
  margin-top: 20px;
  margin-bottom: 30px;
}

.stat-card {
  text-align: center;
  padding: 16px;
  border-radius: 4px;
}

.stat-card .stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-card .stat-label {
  font-size: 14px;
  color: #515a6e;
}

.stat-card.total .stat-value {
  color: #2d8cf0;
}

.stat-card.imported .stat-value {
  color: #19be6b;
}

.stat-card.updated .stat-value {
  color: #ff9900;
}

.stat-card.failed .stat-value {
  color: #ed4014;
}

.error-log {
  margin-top: 30px;
  text-align: left;
}
</style>
