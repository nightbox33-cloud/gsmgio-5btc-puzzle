#!/usr/bin/env python3
"""
GSMG Puzzle Solver - Teoría de Todo
Conecta Matrix, Alice, Mr. Robot, Cosmic Duality y Logic

Basado en el análisis foreNSE completo del puzzle.
"""

import hashlib
import itertools
from datetime import datetime

# ============================================================================
# CONSTANTS - Datos verificados del puzzle
# ============================================================================

# Strings decodificados de SalPhaseIon
SALPHASEION_STRINGS = {
    'matrixsumlist': 'matrixsumlist',
    'enter': 'enter',
    'lastwordsbeforearchichoice': 'lastwordsbeforearchichoice',
    'thispassword': 'thispassword'
}

# Números clave del Architect (Matrix Reloaded)
ARCHITECT_NUMBERS = {
    'individuals': 23,
    'female': 16,
    'male': 7
}

# Fecha única dada por Jrk - Pasaporte de Neo
NEO_PASSPORT_EXPIRY = '09/11/2001'  # DD/MM/YYYY

# ISBN de Cosmic Duality
COSMIC_DUALITY_ISBN = '0809465167'
COSMIC_DUALITY_PAGES = 144

# Offsets mencionados por Jrk
OFFSETS = [-41, -17]

# Typo confirmado
GIVEIT_CORRECT = 'givetit'  # MSG 867

# Pattern 23-16-7 del Architect
PATTERN_23_16_7 = [23, 16, 7]

# ============================================================================
# PRIME NUMBERS - Para dbbib y zero-out
# ============================================================================

def generate_primes(n):
    """Genera los primeros n números primos"""
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes

PRIMES_FIRST_100 = generate_primes(100)

# ============================================================================
# COSMIC DUALITY CHAPTERS - Orden de operaciones
# ============================================================================

COSMIC_DUALITY_CHAPTERS = [
    'The Unity of Opposites',
    'Dualities As Old As Time',
    'The Battle of the Sexes',
    'In The Grasp of Ageless Evil',
    'The Triumph of Good'
]

# ============================================================================
# AES BLOBS - Los tres blobs sin resolver
# ============================================================================

# Estos deberían cargarse de los archivos correspondientes
AES_PHASE32_BLOB = None  # phase3-assets/phase3.2-aes.txt
AES_SALPHASEION_BLOB = None  # salphaseion-assets/
AES_COSMIC_BLOB = None  # gsmg_assets/cosmic_duality.txt

# ============================================================================
# PASSWORD CANDIDATES - Combinaciones para probar AES
# ============================================================================

def generate_password_candidates():
    """
    Genera combinaciones de passwords basadas en el análisis
    """
    
    # Componentes básicos
    components = {
        'givetit': GIVEIT_CORRECT,
        'justonesecond': 'justonesecond',
        'neo_date': NEO_PASSPORT_EXPIRY,
        'isbn': COSMIC_DUALITY_ISBN,
        'pages': str(COSMIC_DUALITY_PAGES),
        'matrixsumlist': SALPHASEION_STRINGS['matrixsumlist'],
        'enter': SALPHASEION_STRINGS['enter'],
        'lastwords': SALPHASEION_STRINGS['lastwordsbeforearchichoice'],
        'thispassword': SALPHASEION_STRINGS['thispassword'],
        'yinyang': 'yinyang',
        'half': 'half',
        'betterhalf': 'betterhalf',
    }
    
    # Variaciones de fecha
    date_variations = [
        '09/11/2001',
        '09112001',
        '11092001',  # US format
        '20010911',
        '11092001',
        '9112001',
        '91101',
    ]
    
    candidates = []
    
    # Combinación 1: givetit + fecha
    for date in date_variations:
        candidates.append(f"{GIVEIT_CORRECT}{date}")
        candidates.append(f"{date}{GIVEIT_CORRECT}")
    
    # Combinación 2: ISBN + componentes
    for comp in ['givetit', 'justonesecond', 'yinyang']:
        candidates.append(f"{COSMIC_DUALITY_ISBN}{comp}")
        candidates.append(f"{comp}{COSMIC_DUALITY_ISBN}")
    
    # Combinación 3: Strings cósmicos concatenados
    cosmic_orderings = [
        ['matrixsumlist', 'enter', 'lastwords', 'thispassword'],
        ['enter', 'matrixsumlist', 'lastwords', 'thispassword'],
        ['lastwords', 'thispassword', 'matrixsumlist', 'enter'],
    ]
    
    for order in cosmic_orderings:
        candidates.append(''.join(components[s] for s in order))
    
    # Combinación 4: Theory of Everything
    # Unificar los 4 pilares
    toe_components = [
        GIVEIT_CORRECT,  # Alice
        'causality',  # Phase 2
        'jacquefresco',  # Phase 3
        'yinyang',  # Cosmic
    ]
    
    for perm in itertools.permutations(toe_components):
        candidates.append(''.join(perm))
    
    # Combinación 5: Con pattern 23-16-7
    for i, num in enumerate(PATTERN_23_16_7):
        candidates.append(f"{GIVEIT_CORRECT}{num}")
        candidates.append(f"{num}{GIVEIT_CORRECT}")
    
    # Combinación 6: Con primos
    for i, prime in enumerate(PRIMES_FIRST_100[:10]):
        candidates.append(f"{GIVEIT_CORRECT}{prime}")
        candidates.append(f"{prime}{GIVEIT_CORRECT}")
    
    # Combinación 7: Half + Better Half
    candidates.append('halfbetterhalf')
    candidates.append('betterhalfhalf')
    candidates.append('halfandbetterhalf')
    
    # Combinación 8: Yin-yang variaciones
    candidates.append('yinyang')
    candidates.append('yingyang')
    candidates.append('yin-yang')
    
    return list(set(candidates))  # Eliminar duplicados

# ============================================================================
# ZERO-OUT OPERATION - Mr. Robot 3.5 kill-process
# ============================================================================

def apply_zero_out(text, positions=None, mask_type='prime'):
    """
    Aplica zero-out a caracteres en posiciones específicas
    
    Args:
        text: Texto original
        positions: Lista de posiciones a zero-outear
        mask_type: 'prime' para posiciones primas, 'date' para máscara de fecha
    """
    result = list(text)
    
    if mask_type == 'prime':
        # Zero-out en posiciones primas (2, 3, 5, 7, 11...)
        primes = generate_primes(len(text))
        for p in primes:
            if p - 1 < len(text):  # -1 porque es índice base 0
                result[p - 1] = '\x00'
    
    elif mask_type == 'date':
        # Usar 09/11/2001 como máscara
        date_nums = [0, 9, 1, 1, 2, 0, 0, 1]
        for i, num in enumerate(date_nums):
            if num > 0 and num - 1 < len(text):
                result[num - 1] = '\x00'
    
    elif positions:
        # Posiciones específicas
        for pos in positions:
            if 0 <= pos < len(text):
                result[pos] = '\x00'
    
    return ''.join(result)

# ============================================================================
# LAST WORDS EXTRACTION - "before archi choice"
# ============================================================================

def extract_last_words(source='movie'):
    """
    Extrae las "últimas palabras antes de la elección del Architect"
    
    Args:
        source: 'movie' (película), 'puzzle' (texto del puzzle), 'prime' (posiciones 23-16-7)
    """
    
    if source == 'movie':
        # Frase del Architect antes de mostrar las puertas
        return "wherein the fundamental flaw is ultimately expressed and the anomaly revealed as both beginning and end"
    
    elif source == 'puzzle':
        # Texto del puzzle antes de ciaobellao
        # Esto debería extraerse del texto VIC decodificado
        return "INCASEYOUMANAGETOCRACKTHIS THEPRIVATEKEYSBELONGTOHALFANDBETTERHALF"
    
    elif source == 'prime':
        # Extraer caracteres en posiciones 23, 16, 7
        # Esto depende del texto de entrada (dbbib o faed)
        return PATTERN_23_16_7
    
    return None

# ============================================================================
# AES DECRYPTION - Probar passwords
# ============================================================================

def try_aes_decrypt(encrypted_b64, password):
    """
    Intenta descifrar un blob AES con OpenSSL
    
    Args:
        encrypted_b64: Blob en base64
        password: Password candidato
    
    Returns:
        Texto descifrado o None si falla
    """
    import subprocess
    import tempfile
    
    # Generar SHA256 del password
    key = hashlib.sha256(password.encode()).hexdigest()
    
    # Crear archivo temporal con el blob
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.b64') as f:
        f.write(encrypted_b64)
        temp_file = f.name
    
    try:
        # Comando OpenSSL
        cmd = [
            'openssl', 'enc', '-aes-256-cbc', '-d', '-a',
            '-in', temp_file,
            '-K', key,
            '-iv', '0' * 32  # IV cero (común en puzzles)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        
    except Exception as e:
        pass
    
    finally:
        import os
        os.unlink(temp_file)
    
    return None

# ============================================================================
# YIN-YANG ECC - Combinar mitades
# ============================================================================

def combine_yin_yang_ecc():
    """
    Combina las dos mitades ECC (Y y -Y del mismo punto X)
    
    Direcciones:
    - 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe (uncompressed)
    - 17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa (compressed, post-halving)
    """
    
    # Pubkey verificado
    pubkey_uncompressed = '04f4d1bb...'  # Completar con pubkey real
    pubkey_compressed = '03f4d1bb...'  # Completar con pubkey real
    
    # En ECC, compressed = 02/03 + X
    # uncompressed = 04 + X + Y
    # better half = 02/03 + X + (-Y mod p)
    
    # La clave privada es la misma para ambas formas
    # Solo cambia la representación del pubkey
    
    return {
        'uncompressed': pubkey_uncompressed,
        'compressed': pubkey_compressed,
        'note': 'Same private key, different pubkey representations'
    }

# ============================================================================
# MAIN SOLVER
# ============================================================================

def main():
    print("=" * 70)
    print("GSMG PUZZLE SOLVER - TEORÍA DE TODO")
    print("=" * 70)
    print()
    
    # 1. Generar candidatos a password
    print("[1] Generando candidatos a password...")
    candidates = generate_password_candidates()
    print(f"    {len(candidates)} candidatos generados")
    print()
    
    # 2. Mostrar combinaciones clave
    print("[2] Combinaciones clave:")
    for i, cand in enumerate(candidates[:20]):
        print(f"    {i+1}. {cand}")
    if len(candidates) > 20:
        print(f"    ... y {len(candidates) - 20} más")
    print()
    
    # 3. Zero-out examples
    print("[3] Ejemplos de zero-out:")
    test_text = "BTCSEED" + "A" * 100
    zeroed_prime = apply_zero_out(test_text, mask_type='prime')
    zeroed_date = apply_zero_out(test_text, mask_type='date')
    print(f"    Original: {test_text[:20]}...")
    print(f"    Zero-out prime: {zeroed_prime[:20]}...")
    print(f"    Zero-out date: {zeroed_date[:20]}...")
    print()
    
    # 4. Last words extraction
    print("[4] Extracción de 'last words before archichoice':")
    for source in ['movie', 'puzzle', 'prime']:
        words = extract_last_words(source)
        print(f"    {source}: {words[:50] if words else 'N/A'}...")
    print()
    
    # 5. Yin-yang ECC
    print("[5] Yin-yang ECC:")
    ecc_result = combine_yin_yang_ecc()
    print(f"    Uncompressed: {ecc_result['uncompressed'][:20]}...")
    print(f"    Compressed: {ecc_result['compressed'][:20]}...")
    print(f"    Note: {ecc_result['note']}")
    print()
    
    # 6. Próximos pasos
    print("[6] Próximos pasos:")
    print("    - Cargar blobs AES reales de los archivos")
    print("    - Probar cada candidato con OpenSSL")
    print("    - Verificar zero-out sobre faed completo")
    print("    - Aplicar estructura de capítulos Cosmic Duality")
    print()
    
    print("=" * 70)
    print("Script listo para ejecutar. Cargar blobs AES y probar.")
    print("=" * 70)

if __name__ == '__main__':
    main()
