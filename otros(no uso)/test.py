from prompt_toolkit import prompt

texto_completo = prompt(">> ", multiline=True)

print("\n--- Tu texto completo ---")
print(texto_completo)