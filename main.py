import wx
import requests
import datetime
import time
from wx.grid import Grid
import json

class TestModelDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="测试模型", size=(400, 300))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 模型输入
        model_box = wx.BoxSizer(wx.HORIZONTAL)
        model_label = wx.StaticText(panel, label="模型名称:")
        self.model_input = wx.TextCtrl(panel, value="gpt-3.5-turbo")
        model_box.Add(model_label, 0, wx.ALL | wx.CENTER, 5)
        model_box.Add(self.model_input, 1, wx.ALL | wx.EXPAND, 5)
        
        # 测试内容
        content_label = wx.StaticText(panel, label="测试内容:")
        self.content_input = wx.TextCtrl(panel, value="say this is test!", 
                                       style=wx.TE_MULTILINE)
        
        # 按钮
        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, wx.ID_OK, "测试")
        cancel_button = wx.Button(panel, wx.ID_CANCEL, "取消")
        btn_box.Add(ok_button, 1, wx.ALL, 5)
        btn_box.Add(cancel_button, 1, wx.ALL, 5)
        
        vbox.Add(model_box, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(content_label, 0, wx.ALL, 5)
        vbox.Add(self.content_input, 1, wx.ALL | wx.EXPAND, 5)
        vbox.Add(btn_box, 0, wx.ALL | wx.CENTER, 5)
        
        panel.SetSizer(vbox)

class APIFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='API Key Detector', size=(800, 600))
        self.api_key = None
        self.url = None
        self.language = "中文"
        
        # 初始化UI组件
        self.init_ui()
        
        # 设置默认语言
        self.update_language()
        
    def init_ui(self):
        """初始化所有UI组件"""
        # 创建主面板
        self.panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)
        
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(panel_sizer)
        main_sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 5)
        
        # 初始化各个区域
        self.init_menu()
        config_sizer = self.init_config_section()
        button_sizer = self.init_button_section()
        grid_sizer = self.init_grid_section()
        
        # 添加所有控件到面板布局
        panel_sizer.Add(config_sizer, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(button_sizer, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(grid_sizer, 1, wx.ALL | wx.EXPAND, 5)
    
    def init_menu(self):
        """初始化菜单栏"""
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        language_menu = wx.Menu()
        
        # 语言选项
        self.chinese_item = language_menu.AppendRadioItem(-1, "中文")
        self.english_item = language_menu.AppendRadioItem(-1, "English")
        
        # 绑定语言菜单事件
        self.Bind(wx.EVT_MENU, lambda evt: self.on_language_change("中文"), self.chinese_item)
        self.Bind(wx.EVT_MENU, lambda evt: self.on_language_change("English"), self.english_item)
        
        file_menu.AppendSubMenu(language_menu, "语言/Language")
        menubar.Append(file_menu, "设置")
        self.SetMenuBar(menubar)
    
    def init_config_section(self):
        """初始化API配置区域"""
        config_box = wx.StaticBox(self.panel, label="API Configuration")
        config_sizer = wx.StaticBoxSizer(config_box, wx.VERTICAL)
        
        # URL输入
        url_sizer = wx.BoxSizer(wx.HORIZONTAL)
        url_label = wx.StaticText(config_box, label="API URL:")
        self.url_input = wx.TextCtrl(config_box)
        url_sizer.Add(url_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        url_sizer.Add(self.url_input, 1, wx.ALL | wx.EXPAND, 5)
        
        # API Key输入
        key_sizer = wx.BoxSizer(wx.HORIZONTAL)
        key_label = wx.StaticText(config_box, label="API Key:")
        self.key_input = wx.TextCtrl(config_box)
        key_sizer.Add(key_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        key_sizer.Add(self.key_input, 1, wx.ALL | wx.EXPAND, 5)
        
        config_sizer.Add(url_sizer, 0, wx.EXPAND | wx.ALL, 5)
        config_sizer.Add(key_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        return config_sizer
    
    def init_button_section(self):
        """初始化按钮区域"""
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.balance_btn = wx.Button(self.panel, label="获取额度")
        self.models_btn = wx.Button(self.panel, label="获取模型")
        self.test_btn = wx.Button(self.panel, label="模型测试")
        
        for btn in [self.balance_btn, self.models_btn, self.test_btn]:
            button_sizer.Add(btn, 1, wx.ALL | wx.EXPAND, 5)
        
        # 绑定事件
        self.balance_btn.Bind(wx.EVT_BUTTON, self.on_get_balance)
        self.models_btn.Bind(wx.EVT_BUTTON, self.on_get_models)
        self.test_btn.Bind(wx.EVT_BUTTON, self.on_test_model)
        
        return button_sizer
    
    def init_grid_section(self):
        """初始化表格和输出区域"""
        grid_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 表格
        self.grid = Grid(self.panel)
        self.grid.CreateGrid(0, 2)
        self.grid.SetColLabelValue(0, "类别")
        self.grid.SetColLabelValue(1, "值")
        self.grid.SetMinSize((750, 200))
        
        # 输出区域
        self.output = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        self.output.SetMinSize((750, 150))
        
        grid_sizer.Add(self.grid, 1, wx.ALL | wx.EXPAND, 5)
        grid_sizer.Add(self.output, 1, wx.ALL | wx.EXPAND, 5)
        
        return grid_sizer
    
    def on_language_change(self, lang):
        self.language = lang
        self.update_language()
    
    def update_language(self):
        labels = {
            "中文": {
                "title": "大模型API密钥检测器",
                "balance": "获取额度",
                "models": "获取模型",
                "test": "模型测试",
                "category": "类别",
                "value": "值"
            },
            "English": {
                "title": "LLMs API Key Detector",
                "balance": "Get Balance",
                "models": "Get Models",
                "test": "Test Model",
                "category": "Category",
                "value": "Value"
            }
        }
        
        self.SetTitle(labels[self.language]["title"])
        self.balance_btn.SetLabel(labels[self.language]["balance"])
        self.models_btn.SetLabel(labels[self.language]["models"])
        self.test_btn.SetLabel(labels[self.language]["test"])
        self.grid.SetColLabelValue(0, labels[self.language]["category"])
        self.grid.SetColLabelValue(1, labels[self.language]["value"])
    
    def log(self, message, clear=False):
        if clear:
            self.output.SetValue("")
        self.output.AppendText(message + "\n")
    
    def update_grid(self, data, clear=True):
        if clear:
            self.grid.ClearGrid()
            if self.grid.GetNumberRows() > 0:
                self.grid.DeleteRows(0, self.grid.GetNumberRows())
        
        for i, (key, value) in enumerate(data):
            self.grid.AppendRows(1)
            self.grid.SetCellValue(i, 0, str(key))
            self.grid.SetCellValue(i, 1, str(value))
            
            # 设置交替行颜色
            if i % 2 == 0:
                self.grid.SetCellBackgroundColour(i, 0, wx.Colour(240, 240, 240))
                self.grid.SetCellBackgroundColour(i, 1, wx.Colour(240, 240, 240))
            
            # 如果是额度相关的行，设置特殊颜色
            if "剩余" in str(key):
                self.grid.SetCellTextColour(i, 1, wx.Colour(0, 128, 0))  # 绿色
            elif "已使用" in str(key):
                self.grid.SetCellTextColour(i, 1, wx.Colour(200, 0, 0))  # 红色
            elif "总额度" in str(key):
                self.grid.SetCellTextColour(i, 1, wx.Colour(0, 0, 200))  # 蓝色
        
        # 自适应调整列宽
        self.grid.AutoSizeColumns()
        # 为每列添加一些额外的空间，避免文本过于紧凑
        for col in range(self.grid.GetNumberCols()):
            current_width = self.grid.GetColSize(col)
            self.grid.SetColSize(col, current_width + 20)
        
        # 确保列宽不超过grid的可见区域
        grid_width = self.grid.GetSize().GetWidth()
        total_width = sum(self.grid.GetColSize(col) for col in range(self.grid.GetNumberCols()))
        if total_width < grid_width:
            extra_space = (grid_width - total_width) // self.grid.GetNumberCols()
            for col in range(self.grid.GetNumberCols()):
                current_width = self.grid.GetColSize(col)
                self.grid.SetColSize(col, current_width + extra_space)
    
    def on_get_balance(self, event):
        self.api_key = self.key_input.GetValue()
        self.url = self.url_input.GetValue()
        
        if not self.api_key or not self.url:
            self.log("请输入API URL和Key")
            return
        
        try:
            headers = {'Authorization': f'Bearer {self.api_key}', "Content-Type": "application/json"}
            
            # 获取订阅信息
            subscription_response = requests.get(f"{self.url}/v1/dashboard/billing/subscription", headers=headers)
            if subscription_response.status_code == 200:
                data = subscription_response.json()
                total = data.get("hard_limit_usd", 0)
            else:
                self.log(f"获取订阅信息失败: {subscription_response.text}")
                return
                
            # 获取使用情况
            start_date = (datetime.datetime.now() - datetime.timedelta(days=99)).strftime("%Y-%m-%d")
            end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            billing_response = requests.get(
                f"{self.url}/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}",
                headers=headers
            )
            
            if billing_response.status_code == 200:
                data = billing_response.json()
                total_usage = data.get("total_usage", 0) / 100
            else:
                self.log(f"获取使用情况失败: {billing_response.text}")
                return
                
            remaining = total - total_usage
            
            # 格式化金额显示
            def format_amount(amount):
                return f"{amount:,.2f} USD"
            
            # 更新表格
            balance_data = [
                ("总额度", format_amount(total)),
                ("已使用", format_amount(total_usage)),
                ("剩余", format_amount(remaining))
            ]
            self.update_grid(balance_data)
            self.log("获取额度信息成功")
            
        except Exception as e:
            self.log(f"发生错误: {str(e)}")
    
    def on_get_models(self, event):
        self.api_key = self.key_input.GetValue()
        self.url = self.url_input.GetValue()
        
        if not self.api_key or not self.url:
            self.log("请输入API URL和Key")
            return
        
        try:
            headers = {'Authorization': f'Bearer {self.api_key}', "Content-Type": "application/json"}
            response = requests.get(f"{self.url}/v1/models", headers=headers)
            
            if response.status_code == 200:
                models = response.json().get('data', [])
                model_data = [(model['id'], model.get('owned_by', 'Unknown')) for model in models]
                self.update_grid(model_data)
                self.log(f"成功获取到 {len(models)} 个模型")
            else:
                self.log(f"获取模型失败: {response.text}")
        
        except Exception as e:
            self.log(f"发生错误: {str(e)}")
    
    def on_test_model(self, event):
        dialog = TestModelDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            model = dialog.model_input.GetValue()
            content = dialog.content_input.GetValue()
            self.run_model_test(model, content)
        dialog.Destroy()
    
    def run_model_test(self, model, content):
        self.api_key = self.key_input.GetValue()
        self.url = self.url_input.GetValue()
        
        if not self.api_key or not self.url:
            self.log("请输入API URL和Key")
            return
        
        try:
            headers = {'Authorization': f'Bearer {self.api_key}', "Content-Type": "application/json"}
            data = {
                "model": model,
                "messages": [
                    {"role": "user", "content": content}
                ]
            }
            
            start_time = time.time()
            response = requests.post(f"{self.url}/v1/chat/completions", 
                                  headers=headers, 
                                  json=data)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                response_content = result['choices'][0]['message']['content']
                actual_model = result.get('model', 'unknown')
                
                test_data = [
                    ("请求模型", model),
                    ("实际模型", actual_model),
                    ("响应时间", f"{end_time - start_time:.2f}秒"),
                    ("响应内容", response_content)
                ]
                self.update_grid(test_data)
                self.log("模型测试成功")
            else:
                self.log(f"模型测试失败: {response.text}")
        
        except Exception as e:
            self.log(f"发生错误: {str(e)}")

if __name__ == '__main__':
    app = wx.App()
    frame = APIFrame()
    frame.Show()
    app.MainLoop()
