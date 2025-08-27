import requests
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class ErnieService:
    def __init__(self):
        # 从settings中获取API密钥
        self.api_key = getattr(settings, 'ERNIE_API_KEY', None)
        # 使用正确的基础URL
        self.base_url = "https://www.blueshirtmap.com"
        self.access_token = None
        
        # 记录API密钥信息（仅记录长度，不记录具体内容以保证安全）
        logger.info(f"ERNIE API Key length: {len(self.api_key) if self.api_key else 0}")
        
    def _get_access_token(self):
        """
        获取访问令牌 - 对于这个API，可能不需要单独获取token
        """
        if not self.api_key:
            raise Exception("请在settings.py中配置ERNIE_API_KEY")
            
        # 对于这个API，API Key就是认证方式，不需要额外获取access_token
        self.access_token = self.api_key
        return self.access_token
    
    def chat_completion(self, prompt, model="gpt-3.5-turbo"):
        """
        调用新的AI API进行对话
        
        Args:
            prompt (str): 用户输入的提示
            model (str): 使用的模型，默认为gpt-3.5-turbo
            
        Returns:
            str: AI回复的内容
        """
        try:
            # 获取访问令牌
            if not self.access_token:
                self._get_access_token()
                
            # API端点
            url = f"{self.base_url}/v1/chat/completions"
            
            # 构造请求消息
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2048
            }
            
            # 设置请求头
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.access_token}'
            }
            
            logger.info(f"开始调用AI API，模型: {model}，URL: {url}")
            response = requests.post(url, json=payload, headers=headers, timeout=120)
            logger.info(f"AI API调用完成，状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                # 提取回复内容
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    logger.info("AI API调用成功")
                    return content
                else:
                    raise Exception(f"API返回格式错误: {result}")
            else:
                error_text = response.text
                logger.error(f"AI API调用失败，状态码: {response.status_code}，响应内容: {error_text}")
                
                # 特殊处理401错误
                if response.status_code == 401:
                    raise Exception("API认证失败，请检查API Key是否正确")
                elif response.status_code == 404:
                    raise Exception(f"API端点未找到，请检查URL是否正确: {url}")
                    
                raise Exception(f"API调用失败: {response.status_code} - {error_text}")
                
        except requests.exceptions.ConnectionError as e:
            logger.error(f"网络连接错误: {str(e)}")
            raise Exception(f"网络连接错误，请检查网络连接是否正常")
        except requests.exceptions.Timeout as e:
            logger.error(f"请求超时: {str(e)}")
            raise Exception(f"请求超时，请稍后重试")
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求异常: {str(e)}")
            raise Exception(f"网络请求异常: {str(e)}")
        except Exception as e:
            logger.error(f"AI API调用出错: {str(e)}")
            raise Exception(f"AI API调用出错: {str(e)}")

    def chat_completion_stream(self, prompt, model="gpt-3.5-turbo"):
        """
        调用新的AI API进行流式对话
        
        Args:
            prompt (str): 用户输入的提示
            model (str): 使用的模型，默认为gpt-3.5-turbo
            
        Yields:
            str: AI回复的内容片段
        """
        try:
            # 获取访问令牌
            if not self.access_token:
                self._get_access_token()
                
            # API端点
            url = f"{self.base_url}/v1/chat/completions"
            
            # 构造请求消息
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2048,
                "stream": True  # 启用流式输出
            }
            
            # 设置请求头
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'text/event-stream',
                'Authorization': f'Bearer {self.access_token}'
            }
            
            logger.info(f"开始调用AI流式API，模型: {model}，URL: {url}")
            
            # 发送流式请求
            response = requests.post(url, json=payload, headers=headers, timeout=120, stream=True)
            
            if response.status_code == 200:
                # 处理流式响应
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith('data: '):
                            data = decoded_line[6:]  # 移除 'data: ' 前缀
                            if data != '[DONE]':
                                try:
                                    json_data = json.loads(data)
                                    if "choices" in json_data and len(json_data["choices"]) > 0:
                                        delta = json_data["choices"][0].get("delta", {})
                                        content = delta.get("content", "")
                                        if content:
                                            yield content
                                except json.JSONDecodeError:
                                    # 如果不是JSON格式，跳过该行
                                    continue
                logger.info("AI流式API调用完成")
            else:
                error_text = response.text
                logger.error(f"AI流式API调用失败，状态码: {response.status_code}，响应内容: {error_text}")
                
                # 特殊处理401错误
                if response.status_code == 401:
                    raise Exception("API认证失败，请检查API Key是否正确")
                elif response.status_code == 404:
                    raise Exception(f"API端点未找到，请检查URL是否正确: {url}")
                    
                raise Exception(f"API调用失败: {response.status_code} - {error_text}")
                
        except requests.exceptions.ConnectionError as e:
            logger.error(f"网络连接错误: {str(e)}")
            raise Exception(f"网络连接错误，请检查网络连接是否正常")
        except requests.exceptions.Timeout as e:
            logger.error(f"请求超时: {str(e)}")
            raise Exception(f"请求超时，请稍后重试")
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求异常: {str(e)}")
            raise Exception(f"网络请求异常: {str(e)}")
        except Exception as e:
            logger.error(f"AI流式API调用出错: {str(e)}")
            raise Exception(f"AI流式API调用出错: {str(e)}")
