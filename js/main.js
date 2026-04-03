const examples = {
    'ex1': `# 练习1：变量与输出
name = "张三"
age = 14
school = "某某中学"

print("个人信息：")
print(f"姓名：{name}")
print(f"年龄：{age}")
print(f"学校：{school}")`,
    
    'ex2': `# 练习2：数学计算
import math

radius = 5
area = math.pi * radius ** 2
circumference = 2 * math.pi * radius

print(f"圆的半径：{radius}")
print(f"圆的面积：{area:.2f}")
print(f"圆的周长：{circumference:.2f}")`,
    
    'ex3': `# 练习3：条件判断
score = int(input("请输入成绩："))

if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")`,
    
    'ex4': `# 练习4：循环结构 - 打印乘法口诀表
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j}", end="  ")
    print()`,
    
    'ex5': `# 练习5：函数定义 - 计算器
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "错误：除数不能为零"
    return a / b

num1 = 10
num2 = 5
print(f"{num1} + {num2} = {add(num1, num2)}")
print(f"{num1} - {num2} = {subtract(num1, num2)}")
print(f"{num1} × {num2} = {multiply(num1, num2)}")
print(f"{num1} ÷ {num2} = {divide(num1, num2)}")`,
    
    'ex6': `# 练习6：列表操作 - 学生成绩管理系统
scores = [85, 92, 78, 90, 88, 95, 80]

print("学生成绩：", scores)
print("平均分：", sum(scores) / len(scores))
print("最高分：", max(scores))
print("最低分：", min(scores))
print("90分以上的人数：", len([s for s in scores if s >= 90]))

scores.sort()
print("成绩排序（升序）：", scores)`,
    
    'ex7': `# 练习7：简单日记程序
# 注意：由于浏览器安全限制，文件写入功能需要后端支持
# 这里演示内存中的日记记录

diary = []

def add_diary(date, content):
    diary.append({"date": date, "content": content})
    print("日记已保存！")

def show_diaries():
    print("\\n=== 日记列表 ===")
    for i, entry in enumerate(diary, 1):
        print(f"\\n日记 {i} - {entry['date']}")
        print(entry['content'])

add_diary("2024-01-15", "今天学习了Python列表操作，很有趣！")
add_diary("2024-01-16", "完成了计算器程序，感觉很有成就感！")

show_diaries()`
};

const exampleCodes = {
    'basic': `# 基础示例：打印欢迎信息
print("欢迎学习Python编程！")

# 变量定义和使用
name = "小明"
age = 14
print(f"我叫{name}，今年{age}岁")

# 简单计算
num1 = 10
num2 = 20
result = num1 + num2
print(f"{num1} + {num2} = {result}")`,
    
    'loop': `# 循环示例：打印1-10
for i in range(1, 11):
    print(i)

# 计算1-100的和
total = 0
for i in range(1, 101):
    total += i
print(f"1到100的和是：{total}")`,
    
    'function': `# 函数示例：定义和使用函数
def greet(name):
    """向指定的人问好"""
    return f"你好，{name}！"

def add(a, b):
    """计算两个数的和"""
    return a + b

# 使用函数
print(greet("张三"))
print(f"5 + 3 = {add(5, 3)}")`
};

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    document.getElementById(sectionId).classList.add('active');
    
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`[href="#${sectionId}"]`).classList.add('active');
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

document.querySelectorAll('.chapter-item').forEach(item => {
    item.addEventListener('click', function() {
        const chapter = this.getAttribute('data-chapter');
        
        document.querySelectorAll('.chapter-list .chapter-item').forEach(i => {
            i.classList.remove('active');
        });
        this.classList.add('active');
        
        document.querySelectorAll('.chapter-section').forEach(section => {
            section.classList.remove('active');
        });
        const targetSection = document.querySelector(`.chapter-section[data-chapter="${chapter}"]`);
        if (targetSection) {
            targetSection.classList.add('active');
        }
    });
});

function showExerciseLevel(level) {
    document.querySelectorAll('.exercise-level').forEach(el => {
        el.classList.remove('active');
    });
    document.querySelector(`[data-level="${level}"]`).classList.add('active');
    
    document.querySelectorAll('.exercise-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
}

function loadExercise(exerciseId) {
    document.getElementById('code-editor').value = examples[exerciseId] || '练习代码加载中...';
}

function showExample(type) {
    document.getElementById('code-editor').value = exampleCodes[type] || '示例代码加载中...';
}

async function executeCode() {
    // 检查登录状态
    const userStr = localStorage.getItem('user');
    if (!userStr) {
        showToast('请先登录后再运行代码！', 'error');
        toggleLoginModal();
        return;
    }

    const code = document.getElementById('code-editor').value;
    const output = document.getElementById('output');
    
    // 简单的输入预处理：查找有多少个 input() 调用
    let inputs = [];
    const inputMatches = code.match(/input\s*\((.*?)\)/g);
    
    if (inputMatches) {
        output.innerHTML = '';
        for (let i = 0; i < inputMatches.length; i++) {
            // 尝试提取 input 的提示词
            let promptText = "请输入数据：";
            const match = inputMatches[i].match(/input\s*\(\s*['"](.*?)['"]\s*\)/);
            if (match && match[1]) {
                promptText = match[1];
            }
            
            // 在输出区域创建交互式输入框
            const inputContainer = document.createElement('div');
            inputContainer.style.marginBottom = '10px';
            
            const promptSpan = document.createElement('span');
            promptSpan.textContent = promptText + ' ';
            promptSpan.style.color = '#4caf50';
            
            const inputBox = document.createElement('input');
            inputBox.type = 'text';
            inputBox.style.background = 'transparent';
            inputBox.style.border = 'none';
            inputBox.style.borderBottom = '1px solid #4caf50';
            inputBox.style.color = '#fff';
            inputBox.style.outline = 'none';
            inputBox.style.fontFamily = 'monospace';
            inputBox.style.fontSize = '14px';
            inputBox.style.width = '200px';
            
            inputContainer.appendChild(promptSpan);
            inputContainer.appendChild(inputBox);
            output.appendChild(inputContainer);
            
            // 等待用户输入
            const userInput = await new Promise(resolve => {
                inputBox.focus();
                inputBox.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter') {
                        inputBox.disabled = true;
                        resolve(inputBox.value);
                    }
                });
            });
            inputs.push(userInput || '');
        }
        
        const loadingDiv = document.createElement('div');
        loadingDiv.innerHTML = '<span class="loading"></span> 正在执行代码...';
        output.appendChild(loadingDiv);
    } else {
        output.innerHTML = '<span class="loading"></span> 正在执行代码...';
    }
    
    try {
        const response = await fetch('http://localhost:5000/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code, inputs: inputs })
        });
        
        const result = await response.json();
        
        let outputHtml = '';
        
        if (result.output) {
            // 后端执行 input("xxx") 时，也会把 "xxx" 打印到标准输出里
            // 因为我们在前端已经展示过提示词了，所以尝试把后端输出里的提示词过滤掉
            let cleanOutput = result.output;
            if (inputMatches) {
                for (let i = 0; i < inputMatches.length; i++) {
                    let promptText = "";
                    const match = inputMatches[i].match(/input\s*\(\s*['"](.*?)['"]\s*\)/);
                    if (match && match[1]) {
                        promptText = match[1];
                    }
                    if (promptText) {
                        // 替换掉后端输出中的 promptText，并去除多余的首尾换行或空格
                        cleanOutput = cleanOutput.replace(promptText, '');
                    }
                }
            }
            // 使用 trimStart() 去掉字符串开头的空白字符（包括空格和多余的换行）
            outputHtml += cleanOutput.trimStart().replace(/\n/g, '<br>');
        }
        
        if (result.error) {
            let errorMsg = result.error;
            
            if (errorMsg.includes('SyntaxError')) {
                errorMsg = '语法错误：请检查代码语法是否正确';
            } else if (errorMsg.includes('NameError')) {
                errorMsg = '名称错误：变量未定义';
            } else if (errorMsg.includes('TypeError')) {
                errorMsg = '类型错误：数据类型不匹配';
            } else if (errorMsg.includes('IndexError')) {
                errorMsg = '索引错误：列表索引超出范围';
            } else if (errorMsg.includes('ZeroDivisionError')) {
                errorMsg = '除零错误：除数不能为零';
            }
            
            outputHtml += '<span class="error">❌ ' + errorMsg.replace(/\n/g, '<br>') + '</span>';
        }
        
        // 隐藏 loading 动画
        const loadingEl = output.querySelector('.loading');
        if (loadingEl && loadingEl.parentElement && loadingEl.parentElement !== output) {
            loadingEl.parentElement.remove();
        } else if (loadingEl) {
            loadingEl.remove();
        }
        
        // 移除多余的 "正在执行代码..." 文字，并且清空可能由于它留下的多余空白
        output.innerHTML = output.innerHTML.replace('正在执行代码...', '').trim();
        
        if (outputHtml) {
            // 如果原本 output 里面已经有内容了（比如之前的 input 对话框），加个换行或者直接追加
            output.innerHTML += outputHtml;
        } else {
            output.innerHTML += '代码执行完成（无输出）';
        }
        
    } catch (error) {
        output.innerHTML = '<span class="error">❌ 无法连接到后端服务器，请确保后端已启动！</span>';
    }
}

function clearCode() {
    document.getElementById('code-editor').value = '';
    document.getElementById('output').innerHTML = '代码运行结果将显示在这里...';
}

let isLoginMode = true;

function toggleLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal.style.display === 'flex') {
        modal.style.display = 'none';
    } else {
        modal.style.display = 'flex';
    }
}

// 优雅的 Toast 提示功能
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    // 触发重绘以应用过渡动画
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);

    // 3秒后移除
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300); // 等待过渡动画结束
    }, 3000);
}

function handleProfileClick(event) {
    const userStr = localStorage.getItem('user');
    const dropdown = document.getElementById('userDropdown');
    
    if (userStr) {
        // 已登录状态，切换下拉菜单显示/隐藏
        dropdown.classList.toggle('show');
    } else {
        // 未登录状态，弹出登录框
        toggleLoginModal();
    }
}

// 点击页面其他区域隐藏下拉菜单
window.onclick = function(event) {
    if (!event.target.closest('.user-profile')) {
        const dropdown = document.getElementById('userDropdown');
        if (dropdown && dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
}

function logout(event) {
    event.stopPropagation(); // 阻止事件冒泡触发 handleProfileClick
    localStorage.removeItem('user');
    document.getElementById('userDropdown').classList.remove('show');
    updateUserDisplay();
    showToast('已退出登录', 'info');
}

function toggleMode() {
    isLoginMode = !isLoginMode;
    const title = document.getElementById('modalTitle');
    const btn = document.getElementById('submitBtn');
    const switchMode = document.querySelector('.switch-mode');
    
    if (isLoginMode) {
        title.textContent = '用户登录';
        btn.textContent = '登录';
        switchMode.textContent = '没有账号？点击注册';
    } else {
        title.textContent = '用户注册';
        btn.textContent = '注册';
        switchMode.textContent = '已有账号？点击登录';
    }
}

async function handleLoginRegister() {
    const usernameInput = document.getElementById('username').value;
    const passwordInput = document.getElementById('password').value;
    
    if (!usernameInput || !passwordInput) {
        showToast('请输入用户名和密码！', 'error');
        return;
    }
    
    const endpoint = isLoginMode ? '/api/login' : '/api/register';
    
    try {
        const response = await fetch(`http://localhost:5000${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: usernameInput, password: passwordInput })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            if (isLoginMode) {
                // 登录成功
                localStorage.setItem('user', JSON.stringify(result.user));
                updateUserDisplay();
                toggleLoginModal();
            } else {
                // 注册成功，切换到登录模式
                toggleMode();
            }
        } else {
            showToast(result.message || '操作失败', 'error');
        }
    } catch (error) {
        showToast('网络错误，请确保后端服务已启动', 'error');
    }
}

function updateUserDisplay() {
    const userStr = localStorage.getItem('user');
    const userNameDisplay = document.getElementById('userNameDisplay');
    const avatar = document.querySelector('.user-profile .avatar');
    
    if (userStr) {
        try {
            const user = JSON.parse(userStr);
            userNameDisplay.textContent = user.username;
            // 截取用户名的第一个字（转为大写，适用于英文和中文）作为头像内容
            if (user.username && avatar) {
                avatar.textContent = user.username.charAt(0).toUpperCase();
            }
        } catch(e) {
            userNameDisplay.textContent = '未登录';
            if (avatar) avatar.textContent = 'U';
        }
    } else {
        userNameDisplay.textContent = '未登录';
        if (avatar) avatar.textContent = 'U';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    updateUserDisplay();
    
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('href').substring(1);
            showSection(target);
        });
    });
    
    const statusElement = document.getElementById('status-text');
    if (statusElement) {
        statusElement.textContent = 'Python环境已就绪';
    }
    
    const dotElement = document.querySelector('.status-dot');
    if (dotElement) {
        dotElement.style.backgroundColor = '#4caf50';
    }
    
    document.querySelectorAll('button, .nav-link, .exercise-item, .resource-item, .chapter-item').forEach(element => {
        element.addEventListener('mouseenter', function() {
            if (!this.style.transform || this.style.transform === 'none') {
            }
        });
        
        element.addEventListener('mouseleave', function() {
        });
    });
    
    document.querySelectorAll('button, .nav-link').forEach(element => {
        element.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.97)';
        });
        
        element.addEventListener('mouseup', function() {
            this.style.transform = 'scale(1)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
});

document.querySelectorAll('.exercise-item').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.exercise-item').forEach(i => {
            i.style.background = '#fafafa';
            i.style.borderLeftColor = '#90caf9';
        });
        this.style.background = '#e3f2fd';
        this.style.borderLeftColor = '#1e88e5';
    });
});
