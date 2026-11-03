import pytest
from unittest.mock import MagicMock
from pedido.pedido import Item, Pedido, contar_frete_gratis


# =============================================================
# EXEMPLO — um teste pronto, para você copiar o formato
# =============================================================

def test_exemplo_quantidade_total(pedido_pequeno):
    # 1 café + 2 pães de queijo = 3 unidades
    assert pedido_pequeno.quantidade_total() == 3


# =============================================================
# PARTE 1 — Encontre os bugs
# Escreva um teste para cada bug. Cada teste deve FALHAR
# no código original. Não altere src/pedido/pedido.py ainda.
# =============================================================

def test_bug1_subtotal_considera_quantidade(pedido_pequeno):
    # 1 x 6,00 + 2 x 4,50 = 15,00
    assert pedido_pequeno.subtotal() == 15.0


def test_bug2_frete_gratis_com_exatamente_50():
    pedido = Pedido("Carla", [Item("Combo", 50.0, 1)])
    assert pedido.tem_frete_gratis() is True


def test_bug3_item_mais_barato(pedido_pequeno):
    assert pedido_pequeno.item_mais_barato().nome == "Pão de queijo"


def test_bug4_total_com_desconto_subtrai_percentual():
    pedido = Pedido("Carla", [Item("Combo", 100.0, 1)])
    assert pedido.total_com_desconto(10) == 90.0




# =============================================================
# PARTE 2 — Implemente com TDD
# Siga o ciclo: 🔴 escreva o teste → 🟢 implemente → 🟡 refatore
# =============================================================

# Requisito 1 — contar_frete_gratis(pedidos) -> int
# Escreva os testes ANTES de implementar a função



def test_req1_todos_os_pedidos_com_frete_gratis(pedido_grande):
    outro = Pedido("Carla", [Item("Combo", 50.0, 1)])
    assert contar_frete_gratis([pedido_grande, outro]) == 2


def test_req1_nenhum_pedido_com_frete_gratis(pedido_pequeno):
    outro = Pedido("Carla", [Item("Suco", 8.0, 2)])
    assert contar_frete_gratis([pedido_pequeno, outro]) == 0


def test_req1_lista_mista(pedido_pequeno, pedido_grande):
    assert contar_frete_gratis([pedido_pequeno, pedido_grande]) == 1


def test_req1_lista_vazia_retorna_zero():
    assert contar_frete_gratis([]) == 0


# Requisito 2 — situacao(unidades_indisponiveis) -> str
# Escreva os testes ANTES de implementar o método



def test_req2_tudo_disponivel_abaixo_de_50_confirmado(pedido_pequeno):
    assert pedido_pequeno.situacao(0) == "Confirmado"


def test_req2_tudo_disponivel_a_partir_de_50_frete_gratis(pedido_grande):
    # 2 x 22,00 + 2 x 7,00 + 1 x 15,00 = 73,00
    assert pedido_grande.situacao(0) == "Confirmado com frete grátis"


def test_req2_mais_de_25_porcento_indisponivel_cancela_mesmo_com_frete(pedido_grande):
    # 2 de 5 unidades = 40% indisponível
    assert pedido_grande.situacao(2) == "Cancelado por falta de estoque"


def test_req2_exatamente_25_porcento_segue_para_regra_do_frete():
    # 4 unidades, 1 indisponível = 25%; subtotal 58,00
    pedido = Pedido("Carla", [Item("X-burguer", 22.0, 2), Item("Refrigerante", 7.0, 2)])
    assert pedido.situacao(1) == "Confirmado com frete grátis"


def test_req2_pouco_acima_de_25_porcento_cancela():
    # 7 unidades, 2 indisponíveis = 28,6%
    pedido = Pedido("Carla", [Item("Pastel", 10.0, 7)])
    assert pedido.situacao(2) == "Cancelado por falta de estoque"


# Requisito 3 — sugerir_frete_gratis(sms_service) -> None
# Use MagicMock para simular o serviço de SMS
# Escreva os testes ANTES de implementar o método

def test_req3_abaixo_de_50_aciona_sms_com_valor_faltante(pedido_pequeno):
    sms_service = MagicMock()
    # subtotal 15,00 -> faltam 35,00
    pedido_pequeno.sugerir_frete_gratis(sms_service)
    sms_service.enviar.assert_called_once_with("Bruno", 35.0)


def test_req3_acima_de_50_nao_aciona_sms(pedido_grande):
    sms_service = MagicMock()
    pedido_grande.sugerir_frete_gratis(sms_service)
    sms_service.enviar.assert_not_called()
