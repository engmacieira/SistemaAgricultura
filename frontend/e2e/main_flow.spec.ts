import { test, expect } from '@playwright/test';

test.describe('Fluxo Principal - Sistema Agricultura', () => {
  // Configuração global para esperar requests lentos, se houver
  test.setTimeout(60000);

  test('Deve realizar o fluxo completo: Setup, Login, Fila de Espera, Baixa e Faturamento', async ({ page }) => {
    // --------------------------------------------------------------------------------
    // PASSO 1: Setup via API
    // --------------------------------------------------------------------------------
    // Vamos criar um produtor e um serviço para garantir que existam no banco.
    // Usaremos a API rodando no backend.

    const baseUrl = 'http://127.0.0.1:8000';

    // Realiza o Login via API para pegar o Token
    const loginResponse = await page.request.post(`${baseUrl}/api/usuarios/login`, {
      data: {
        email: 'admin@sunnytech.com',
        password: 'Azulceleste#123'
      }
    });
    expect(loginResponse.ok(), await loginResponse.text()).toBeTruthy();
    const loginData = await loginResponse.json();
    const token = loginData.access_token;

    // Tenta encontrar o produtor, se não existir cria
    let producerData;
    const producersResponse = await page.request.get(`${baseUrl}/api/produtores/?skip=0&limit=100`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const producersList = await producersResponse.json();
    const existingProducer = producersList.items?.find((p: any) => p.cpfCnpj === '111.222.333-44');

    if (existingProducer) {
        producerData = existingProducer;
    } else {
        const producerPayload = {
          name: 'Produtor E2E Test',
          cpfCnpj: '111.222.333-44',
          phone: '11999998888',
          property: 'Fazenda E2E',
          status: 'ATIVO'
        };

        const producerResponse = await page.request.post(`${baseUrl}/api/produtores/`, {
          data: producerPayload,
          headers: { 'Authorization': `Bearer ${token}` }
        });
        expect(producerResponse.ok(), await producerResponse.text()).toBeTruthy();
        producerData = await producerResponse.json();
    }

    // Tenta encontrar o serviço, se não existir cria
    let serviceData;
    const servicesResponse = await page.request.get(`${baseUrl}/api/servicos/?skip=0&limit=100`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const servicesList = await servicesResponse.json();
    const existingService = servicesList.items?.find((s: any) => s.name === 'Serviço E2E Test');

    if (existingService) {
        serviceData = existingService;
    } else {
        const servicePayload = {
          name: 'Serviço E2E Test',
          description: 'Serviço criado pelo script E2E',
          basePrice: 200,
          unit: 'Horas',
          active: true
        };

        const serviceResponse = await page.request.post(`${baseUrl}/api/servicos/`, {
          data: servicePayload,
          headers: { 'Authorization': `Bearer ${token}` }
        });
        expect(serviceResponse.ok(), await serviceResponse.text()).toBeTruthy();
        serviceData = await serviceResponse.json();
    }

    // --------------------------------------------------------------------------------
    // PASSO 2: Login
    // --------------------------------------------------------------------------------
    // O frontend deve estar rodando em http://localhost:3000
    await page.goto('http://localhost:3000');

    // Aguarda o select carregar a lista pública de usuários
    await page.waitForSelector('select[name="email"]');

    // Seleciona o administrador (ou o primeiro usuário disponível)
    // O e-mail usado no script de seed é admin@sunnytech.com
    await page.selectOption('select[name="email"]', 'admin@sunnytech.com');

    // Preenche a senha
    await page.fill('input[name="password"]', 'Azulceleste#123');

    // Clica em Acessar Painel
    await page.click('button:has-text("Acessar Painel")');

    // Verifica se redirecionou para o Dashboard
    await expect(page.locator('text=Dashboard').first()).toBeVisible({ timeout: 15000 });
    await expect(page.url()).toContain('/dashboard');

    // --------------------------------------------------------------------------------
    // PASSO 3: Fluxo Principal (Fila de Espera -> Baixa)
    // --------------------------------------------------------------------------------
    // Ir para a Fila de Espera (Agendamentos)
    await page.click('a[href="/agendamentos"]');

    // 1. Criar uma Nova Solicitação
    await page.click('button:has-text("Nova Solicitação")');
    await expect(page.locator('h2:has-text("Nova Solicitação na Fila")')).toBeVisible();

    // Seleciona o Produtor de Teste recém criado
    await page.selectOption('select:has-text("Produtor")', producerData.id);

    // Preenche os outros campos
    await page.fill('textarea', 'Solicitação de teste E2E');

    // Salva a solicitação
    await page.click('button:has-text("Adicionar à Fila")');

    // Aguarda o modal fechar e a lista atualizar
    await expect(page.locator('text=Solicitação de teste E2E')).toBeVisible();

    // 2. Mudar a aba para "Pendente" e Iniciar (Mudar para Em Andamento)
    // O botão "Iniciar" está no card do produtor
    const cardLocator = page.locator('.bg-white', { hasText: 'Produtor E2E Test' }).first();
    await cardLocator.locator('button:has-text("Iniciar")').click();

    // 3. Ir para "Em Andamento" e dar Baixa
    await page.click('button:has-text("Em Andamento")');

    // O card deve estar aqui agora
    const inProgressCard = page.locator('.bg-white', { hasText: 'Produtor E2E Test' }).first();
    await expect(inProgressCard).toBeVisible();

    // Clica em Dar Baixa
    await inProgressCard.locator('button:has-text("Dar Baixa no Serviço")').click();

    // Aguarda o modal abrir
    await expect(page.locator('h2:has-text("Dar Baixa em Serviço")')).toBeVisible();

    // Preenche os dados da baixa
    // Seleciona o Serviço de Teste recém criado
    await page.locator('text=Qual serviço foi realizado?').locator('..').locator('select').selectOption(serviceData.id);
    await page.fill('input[placeholder="Ex: João / Trator 01"]', 'Trator E2E');

    // O campo Qtd. é o primeiro input do tipo number
    const qtyInput = page.locator('input[type="number"]').first();
    await qtyInput.fill('2');

    // Verifica se o total foi calculado (2 * 200 = 400)
    await expect(page.locator('text=R$ 400.00')).toBeVisible();

    // Confirma e gera o pagamento
    await page.click('button:has-text("Confirmar e Gerar Pagamento")');

    // Aguarda ir para a aba Concluído automaticamente
    await expect(page.locator('button.border-blue-500:has-text("Concluídos")')).toBeVisible();
    await expect(page.locator('.bg-white', { hasText: 'Produtor E2E Test' }).first()).toBeVisible();

    // --------------------------------------------------------------------------------
    // PASSO 4: Validação Final (Pagamentos)
    // --------------------------------------------------------------------------------
    // Ir para a tela de Pagamentos
    await page.locator('text=Pagamentos').first().click();

    // Valida se a dívida do Produtor apareceu lá com o valor exato (R$ 400,00)
    await expect(page.locator('text=Produtor E2E Test').first()).toBeVisible();
    await expect(page.locator('text=R$ 400,00').first()).toBeVisible();
  });
});