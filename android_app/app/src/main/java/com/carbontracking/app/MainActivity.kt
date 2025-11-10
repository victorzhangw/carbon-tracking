package com.carbontracking.app

import android.annotation.SuppressLint
import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Bundle
import android.view.KeyEvent
import android.view.View
import android.webkit.*
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private lateinit var progressBar: ProgressBar
    private lateinit var swipeRefreshLayout: SwipeRefreshLayout
    
    // 後端伺服器網址（雲端部署）
    private val SERVER_URL = "https://carbon-tracking.onrender.com/carbon/"
    
    // 本地測試時使用（開發階段）
    // private val SERVER_URL = "http://10.0.2.2:5000/carbon/"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // 初始化 UI 元件
        webView = findViewById(R.id.webview)
        progressBar = findViewById(R.id.progressBar)
        swipeRefreshLayout = findViewById(R.id.swipeRefreshLayout)
        
        // 設定 WebView
        setupWebView()
        
        // 設定下拉重新整理
        setupSwipeRefresh()
        
        // 檢查網路連線
        if (isNetworkAvailable()) {
            loadUrl(SERVER_URL)
        } else {
            showNoInternetDialog()
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        val webSettings: WebSettings = webView.settings
        
        // 啟用 JavaScript
        webSettings.javaScriptEnabled = true
        
        // 啟用 DOM Storage
        webSettings.domStorageEnabled = true
        
        // 啟用資料庫
        webSettings.databaseEnabled = true
        
        // 快取設定
        webSettings.cacheMode = WebSettings.LOAD_DEFAULT
        webSettings.setAppCacheEnabled(true)
        webSettings.setAppCachePath(cacheDir.path)
        
        // 檔案存取
        webSettings.allowFileAccess = true
        webSettings.allowContentAccess = true
        
        // 支援縮放
        webSettings.setSupportZoom(true)
        webSettings.builtInZoomControls = true
        webSettings.displayZoomControls = false
        
        // 自適應螢幕
        webSettings.useWideViewPort = true
        webSettings.loadWithOverviewMode = true
        
        // 混合內容模式（允許 HTTPS 頁面載入 HTTP 資源）
        webSettings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        
        // 設定 User Agent
        webSettings.userAgentString = webSettings.userAgentString + " CarbonTrackingApp/1.0"
        
        // WebViewClient
        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                super.onPageStarted(view, url, favicon)
                progressBar.visibility = View.VISIBLE
            }
            
            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                progressBar.visibility = View.GONE
                swipeRefreshLayout.isRefreshing = false
            }
            
            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                super.onReceivedError(view, request, error)
                if (request?.isForMainFrame == true) {
                    showErrorPage()
                }
            }
            
            override fun shouldOverrideUrlLoading(
                view: WebView?,
                request: WebResourceRequest?
            ): Boolean {
                val url = request?.url.toString()
                
                // 允許內部連結
                if (url.startsWith(SERVER_URL)) {
                    return false
                }
                
                // 外部連結用瀏覽器開啟
                // startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
                // return true
                
                return false
            }
        }
        
        // WebChromeClient（支援 JavaScript 對話框、進度條等）
        webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                super.onProgressChanged(view, newProgress)
                progressBar.progress = newProgress
            }
            
            override fun onJsAlert(
                view: WebView?,
                url: String?,
                message: String?,
                result: JsResult?
            ): Boolean {
                AlertDialog.Builder(this@MainActivity)
                    .setTitle("提示")
                    .setMessage(message)
                    .setPositiveButton("確定") { _, _ -> result?.confirm() }
                    .setCancelable(false)
                    .create()
                    .show()
                return true
            }
            
            override fun onJsConfirm(
                view: WebView?,
                url: String?,
                message: String?,
                result: JsResult?
            ): Boolean {
                AlertDialog.Builder(this@MainActivity)
                    .setTitle("確認")
                    .setMessage(message)
                    .setPositiveButton("確定") { _, _ -> result?.confirm() }
                    .setNegativeButton("取消") { _, _ -> result?.cancel() }
                    .setCancelable(false)
                    .create()
                    .show()
                return true
            }
        }
        
        // 啟用除錯模式（開發時使用）
        WebView.setWebContentsDebuggingEnabled(BuildConfig.DEBUG)
    }
    
    private fun setupSwipeRefresh() {
        swipeRefreshLayout.setColorSchemeResources(
            R.color.primary,
            R.color.primary_dark,
            R.color.accent
        )
        
        swipeRefreshLayout.setOnRefreshListener {
            webView.reload()
        }
    }
    
    private fun loadUrl(url: String) {
        webView.loadUrl(url)
    }
    
    private fun isNetworkAvailable(): Boolean {
        val connectivityManager = getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val network = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(network) ?: return false
        
        return capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) ||
               capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) ||
               capabilities.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET)
    }
    
    private fun showNoInternetDialog() {
        AlertDialog.Builder(this)
            .setTitle("無網路連線")
            .setMessage("請檢查網路連線後重試")
            .setPositiveButton("重試") { _, _ ->
                if (isNetworkAvailable()) {
                    loadUrl(SERVER_URL)
                } else {
                    showNoInternetDialog()
                }
            }
            .setNegativeButton("離開") { _, _ -> finish() }
            .setCancelable(false)
            .create()
            .show()
    }
    
    private fun showErrorPage() {
        val errorHtml = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {
                        font-family: 'Microsoft JhengHei', Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: #F1F8E9;
                        text-align: center;
                        padding: 20px;
                    }
                    .error-container {
                        max-width: 400px;
                    }
                    h1 {
                        color: #689F38;
                        font-size: 3em;
                        margin: 0;
                    }
                    p {
                        color: #666;
                        font-size: 1.1em;
                        margin: 20px 0;
                    }
                    button {
                        background: #8BC34A;
                        color: white;
                        border: none;
                        padding: 12px 30px;
                        border-radius: 4px;
                        font-size: 1em;
                        cursor: pointer;
                    }
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h1>😕</h1>
                    <h2>無法連線</h2>
                    <p>無法連接到伺服器，請檢查：</p>
                    <ul style="text-align: left;">
                        <li>網路連線是否正常</li>
                        <li>伺服器是否運行中</li>
                        <li>網址是否正確</li>
                    </ul>
                    <button onclick="location.reload()">重新載入</button>
                </div>
            </body>
            </html>
        """.trimIndent()
        
        webView.loadDataWithBaseURL(null, errorHtml, "text/html", "UTF-8", null)
    }
    
    // 支援返回鍵
    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {
            webView.goBack()
            return true
        }
        return super.onKeyDown(keyCode, event)
    }
    
    // 儲存和恢復 WebView 狀態
    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        webView.saveState(outState)
    }
    
    override fun onRestoreInstanceState(savedInstanceState: Bundle) {
        super.onRestoreInstanceState(savedInstanceState)
        webView.restoreState(savedInstanceState)
    }
    
    // 暫停和恢復 WebView
    override fun onPause() {
        super.onPause()
        webView.onPause()
    }
    
    override fun onResume() {
        super.onResume()
        webView.onResume()
    }
    
    // 清理資源
    override fun onDestroy() {
        webView.destroy()
        super.onDestroy()
    }
}
