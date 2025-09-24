#!/usr/bin/env python3
"""
🔥 TESTE RÁPIDO DAS OTIMIZAÇÕES AMD
Executa as otimizações mais importantes para AMD sem interface
"""

import os
import sys
import logging
from datetime import datetime

def setup_logging():
    """Configurar logging"""
    log_file = f"logs/amd_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def test_amd_optimizations():
    """🔥 Testar otimizações AMD rapidamente"""
    logger = setup_logging()
    logger.info("🔥 INICIANDO TESTE DE OTIMIZAÇÕES AMD...")
    
    try:
        # Importar módulos
        from optimizer.advanced_optimizer import AdvancedOptimizer
        from optimizer.performance import PerformanceOptimizer
        from optimizer.special_modes import SpecialModes
        
        # Instanciar otimizadores
        advanced_opt = AdvancedOptimizer()
        perf_opt = PerformanceOptimizer()
        special_modes = SpecialModes(advanced_opt)
        
        logger.info("✅ Módulos carregados com sucesso")
        
        # 1. 🚀 Otimizações de energia extremas
        logger.info("🚀 Aplicando configurações de energia gaming extremo...")
        if perf_opt.optimize_power_settings():
            logger.info("✅ Configurações de energia aplicadas")
        else:
            logger.warning("⚠️ Erro nas configurações de energia")
        
        # 2. 🔥 Otimizações gaming extremas
        logger.info("🔥 Aplicando otimizações gaming extremas...")
        if hasattr(perf_opt, 'extreme_gaming_optimization'):
            if perf_opt.extreme_gaming_optimization():
                logger.info("✅ Otimizações gaming extremas aplicadas")
            else:
                logger.warning("⚠️ Erro nas otimizações gaming")
        
        # 3. 🎮 Otimizações específicas AMD
        logger.info("🎮 Aplicando otimizações específicas AMD...")
        if hasattr(advanced_opt, 'optimize_amd_specific'):
            amd_opts = advanced_opt.optimize_amd_specific()
            logger.info(f"✅ {len(amd_opts)} otimizações AMD aplicadas")
            for opt in amd_opts[:5]:  # Mostrar apenas as primeiras 5
                logger.info(f"   • {opt}")
        
        # 4. 🔥 Modo AMD Beast
        logger.info("🔥 Ativando MODO AMD BEAST...")
        result = special_modes.activate_amd_beast_mode()
        if result.get("success"):
            logger.info("✅ MODO AMD BEAST ativado com sucesso!")
            opts = result.get("optimizations", [])
            logger.info(f"✅ {len(opts)} otimizações AMD Beast aplicadas")
        else:
            logger.warning(f"⚠️ Erro no AMD Beast Mode: {result.get('message')}")
        
        # 5. 🎯 Otimizações gaming do advanced_optimizer
        logger.info("🎯 Aplicando otimizações gaming avançadas...")
        gaming_opts = advanced_opt.optimize_gaming_performance()
        logger.info(f"✅ {len(gaming_opts)} otimizações gaming aplicadas")
        
        logger.info("🔥 TESTE CONCLUÍDO COM SUCESSO!")
        logger.info("💪 Sistema AMD otimizado para máxima performance!")
        logger.info("⚠️ RECOMENDADO: Reinicie o sistema para aplicar todas as otimizações")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ERRO CRÍTICO: {str(e)}")
        logger.error("❌ Teste falhou. Verifique os logs para mais detalhes.")
        return False

if __name__ == "__main__":
    print("🔥 OTIMIZADOR PC - TESTE AMD OPTIMIZATIONS")
    print("=" * 50)
    
    if not os.path.exists("optimizer"):
        print("❌ ERRO: Pasta 'optimizer' não encontrada!")
        print("Execute este script na pasta raiz do projeto.")
        sys.exit(1)
    
    success = test_amd_optimizations()
    
    if success:
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("💪 Sistema otimizado para AMD!")
        print("⚠️ Reinicie para aplicar todas as mudanças.")
        input("\nPressione Enter para continuar...")
    else:
        print("\n❌ TESTE FALHOU!")
        print("Verifique os logs para mais informações.")
        input("\nPressione Enter para continuar...")
    
    sys.exit(0 if success else 1)