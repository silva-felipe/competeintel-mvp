'use client';

import { useState } from 'react';
import { searchCompetitors, type SearchRequest, type SearchResponse } from '@/lib/api';

const CATEGORIES = [
  'Padaria',
  'Restaurante',
  'Farmácia',
  'Supermercado',
  'Cafeteria',
  'Academia',
  'Pet Shop',
  'Lanchonete',
];

const CITIES = [
  { name: 'São Paulo', state: 'SP' },
  { name: 'Rio de Janeiro', state: 'RJ' },
  { name: 'Belo Horizonte', state: 'MG' },
  { name: 'Brasília', state: 'DF' },
  { name: 'Curitiba', state: 'PR' },
  { name: 'Porto Alegre', state: 'RS' },
];

export default function Home() {
  const [formData, setFormData] = useState<SearchRequest>({
    category: 'Padaria',
    city: 'São Paulo',
    state: 'SP',
    radius_km: 5,
    max_results: 10,
  });

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Clean up form data - convert empty strings to undefined
      const cleanedData = {
        ...formData,
        business_name: formData.business_name?.trim() || undefined,
        neighborhood: formData.neighborhood?.trim() || undefined,
        cep: formData.cep?.trim() || undefined,
      };

      const data = await searchCompetitors(cleanedData);
      setResults(data);
    } catch (err: any) {
      setError(err.message || 'Erro ao buscar concorrentes');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-white/10 bg-black/20 backdrop-blur-lg">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <span className="text-4xl">📊</span>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              CompeteIntel
            </h1>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-5xl font-extrabold text-white mb-4">
            Conheça Seus <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">Concorrentes</span>
          </h2>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Análise competitiva inteligente para o mercado brasileiro
          </p>
        </div>

        {/* Search Form */}
        <div className="max-w-4xl mx-auto mb-12">
          <form onSubmit={handleSubmit} className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-8 shadow-2xl">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Nome do Seu Negócio (opcional)
                </label>
                <input
                  type="text"
                  value={formData.business_name || ''}
                  onChange={(e) => setFormData({ ...formData, business_name: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition"
                  placeholder="Minha Empresa"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Categoria do Negócio *
                </label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition"
                  required
                >
                  {CATEGORIES.map((cat) => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Cidade *
                </label>
                <select
                  value={formData.city}
                  onChange={(e) => {
                    const city = CITIES.find(c => c.name === e.target.value);
                    setFormData({ ...formData, city: e.target.value, state: city?.state });
                  }}
                  className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition"
                  required
                >
                  {CITIES.map((city) => (
                    <option key={city.name} value={city.name}>{city.name} ({city.state})</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Bairro (opcional)
                </label>
                <input
                  type="text"
                  value={formData.neighborhood || ''}
                  onChange={(e) => setFormData({ ...formData, neighborhood: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition"
                  placeholder="Ex: Vila Madalena, Centro"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  CEP (opcional)
                </label>
                <input
                  type="text"
                  value={formData.cep || ''}
                  onChange={(e) => setFormData({ ...formData, cep: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition"
                  placeholder="00000-000"
                  maxLength={9}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Raio de Busca (km)
                </label>
                <input
                  type="number"
                  min="0.5"
                  max="50"
                  step="0.5"
                  value={formData.radius_km}
                  onChange={(e) => setFormData({ ...formData, radius_km: parseFloat(e.target.value) })}
                  className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 text-white font-bold rounded-lg shadow-lg shadow-cyan-500/50 transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {loading ? 'Analisando...' : 'Buscar Concorrentes 🔍'}
            </button>
          </form>
        </div>

        {/* Error Message */}
        {error && (
          <div className="max-w-4xl mx-auto mb-8 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200">
            <strong>Erro:</strong> {error}
          </div>
        )}

        {/* Results */}
        {results && (
          <div className="max-w-6xl mx-auto space-y-8">
            {/* Summary */}
            <div className="bg-gradient-to-r from-cyan-500/20 to-purple-500/20 border border-white/20 rounded-2xl p-6 backdrop-blur-lg">
              <h3 className="text-2xl font-bold text-white mb-3">Resumo da Análise</h3>
              <p className="text-slate-200 text-lg">{results.analytics.summary}</p>
            </div>

            {/* Market Density */}
            <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6">
              <h3 className="text-xl font-bold text-white mb-4">Densidade de Mercado</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-slate-800/50 rounded-lg p-4">
                  <div className="text-3xl font-bold text-cyan-400">{results.analytics.market_density.total_competitors}</div>
                  <div className="text-sm text-slate-400">Concorrentes</div>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-4">
                  <div className="text-3xl font-bold text-purple-400">{results.analytics.market_density.competitors_per_km2.toFixed(1)}</div>
                  <div className="text-sm text-slate-400">por km²</div>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-4">
                  <div className="text-3xl font-bold text-pink-400">{results.analytics.market_density.density_level}</div>
                  <div className="text-sm text-slate-400">Densidade</div>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-4">
                  <div className="text-3xl font-bold text-orange-400">{results.analytics.market_density.market_saturation_score.toFixed(0)}%</div>
                  <div className="text-sm text-slate-400">Saturação</div>
                </div>
              </div>
            </div>

            {/* KPI Recommendations */}
            {results.analytics.kpi_recommendations.length > 0 && (
              <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6">
                <h3 className="text-xl font-bold text-white mb-4">Recomendações</h3>
                <div className="space-y-4">
                  {results.analytics.kpi_recommendations.map((kpi, idx) => (
                    <div key={idx} className="bg-slate-800/50 rounded-lg p-4 border-l-4 border-cyan-400">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-bold text-white">{kpi.metric}</h4>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${kpi.priority === 'High' ? 'bg-red-500/20 text-red-300' :
                          kpi.priority === 'Medium' ? 'bg-yellow-500/20 text-yellow-300' :
                            'bg-green-500/20 text-green-300'
                          }`}>
                          {kpi.priority}
                        </span>
                      </div>
                      <p className="text-slate-300 text-sm mb-2">{kpi.recommendation}</p>
                      <div className="flex gap-4 text-xs text-slate-400">
                        <span>Atual: <strong className="text-slate-300">{kpi.current_value}</strong></span>
                        <span>Benchmark: <strong className="text-slate-300">{kpi.benchmark_value}</strong></span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Competitors List */}
            <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6">
              <h3 className="text-xl font-bold text-white mb-4">
                Concorrentes Encontrados ({results.total_found})
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {results.competitors.map((comp) => (
                  <div key={comp.id} className="bg-slate-800/50 rounded-lg p-4 hover:bg-slate-800/70 transition border border-white/5">
                    <h4 className="font-bold text-white mb-2">{comp.name}</h4>
                    <div className="space-y-1 text-sm text-slate-300">
                      <div className="flex items-center gap-2">
                        <span>⭐</span>
                        <span>{comp.rating.toFixed(1)} ({comp.review_count} avaliações)</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span>📍</span>
                        <span>{comp.distance_km?.toFixed(1)} km</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span>💰</span>
                        <span>R$ {(comp.estimated_monthly_revenue / 1000).toFixed(0)}k/mês</span>
                      </div>
                      <div className="flex gap-2 mt-2">
                        {comp.online_presence.has_instagram && <span className="text-xs bg-pink-500/20 text-pink-300 px-2 py-1 rounded">Instagram</span>}
                        {comp.online_presence.has_website && <span className="text-xs bg-blue-500/20 text-blue-300 px-2 py-1 rounded">Website</span>}
                        {comp.accepts_pix && <span className="text-xs bg-green-500/20 text-green-300 px-2 py-1 rounded">PIX</span>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 bg-black/20 backdrop-blur-lg mt-20">
        <div className="container mx-auto px-6 py-8 text-center text-slate-400">
          <p>&copy; 2024 CompeteIntel. Feito com ❤️ para o mercado brasileiro 🇧🇷</p>
        </div>
      </footer>
    </div>
  );
}
