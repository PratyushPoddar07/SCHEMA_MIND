import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Database, History, Settings, Menu, X, Plus, Table, Search, Shield, ChevronRight } from 'lucide-react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import toast, { Toaster } from 'react-hot-toast';

import Background3D from '@/components/Background3D';
import QueryInput from '@/components/QueryInput';
import ResultsDisplay from '@/components/ResultsDisplay';
import SchemaVisualizer3D from '@/components/SchemaVisualizer3D';
import { apiService } from '@/services/api';
import { useAppStore } from '@/store';
import type { Query, DatabaseConnection, TableInfo } from '@/types';

export default function Dashboard() {
  const [selectedTable, setSelectedTable] = useState<TableInfo | null>(null);
  const [showSchema, setShowSchema] = useState(false);
  const [isAddDbOpen, setIsAddDbOpen] = useState(false);
  const [newDb, setNewDb] = useState({
    name: '',
    db_type: 'postgresql' as const,
    connection_string: ''
  });

  const {
    selectedDatabase,
    setSelectedDatabase,
    queries,
    addQuery,
    sidebarOpen,
    toggleSidebar
  } = useAppStore();

  const queryClient = useQueryClient();

  // Fetch databases
  const { data: databases } = useQuery({
    queryKey: ['databases'],
    queryFn: apiService.getDatabases,
  });

  // Fetch schema
  const { data: schema } = useQuery({
    queryKey: ['schema', selectedDatabase?.id],
    queryFn: () => apiService.getSchema(selectedDatabase!.id),
    enabled: !!selectedDatabase,
  });

  // Fetch query history
  const { data: queryHistory } = useQuery({
    queryKey: ['query-history', selectedDatabase?.id],
    queryFn: () => apiService.getQueryHistory(selectedDatabase?.id),
    enabled: !!selectedDatabase,
  });

  // Execute query mutation
  const executeMutation = useMutation({
    mutationFn: (query: string) => apiService.executeQuery({
      natural_language_query: query,
      database_id: selectedDatabase!.id,
      include_insights: true,
      explain_sql: true,
    }),
    onSuccess: (data) => {
      addQuery(data);
      queryClient.invalidateQueries({ queryKey: ['query-history'] });
      toast.success('Query executed successfully!');
    },
    onError: (error: any) => {
      console.error('Query Execution Error:', error);
      const msg = error.response?.data?.detail || error.message || JSON.stringify(error);
      toast.error(`Query Failed: ${msg}`);
    },
  });

  // Add database mutation
  const addDbMutation = useMutation({
    mutationFn: apiService.createDatabase,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['databases'] });
      setIsAddDbOpen(false);
      setNewDb({ name: '', db_type: 'postgresql', connection_string: '' });
      toast.success('Database added successfully!');
    },
    onError: (error: any) => {
      console.error('Add DB Error:', error);
      const msg = error.response?.data?.detail || error.message || 'Failed to add database';
      toast.error(`Error: ${msg}`);
    }
  });

  // Auto-select first database
  useEffect(() => {
    if (databases && databases.length > 0 && !selectedDatabase) {
      setSelectedDatabase(databases[0]);
    }
  }, [databases, selectedDatabase, setSelectedDatabase]);

  const handleQuerySubmit = (query: string) => {
    if (!selectedDatabase) {
      toast.error('Please select a database first');
      return;
    }
    executeMutation.mutate(query);
  };

  const handleAddDb = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newDb.name || !newDb.connection_string) {
      toast.error('Please fill in all fields');
      return;
    }
    addDbMutation.mutate(newDb);
  };

  const latestQuery = queries[0];

  return (
    <div className="min-h-screen relative overflow-hidden bg-[#0a0a0f]">
      <Toaster position="top-right" />
      <Background3D />

      <div className="relative z-10 flex flex-col h-screen">
        {/* Header */}
        <header className="glass-effect border-b border-white/10 shrink-0">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <button
                  onClick={toggleSidebar}
                  className="p-2 glass-effect rounded-lg hover:bg-white/10 transition-all"
                >
                  {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
                </button>

                <h1 className="text-2xl font-bold gradient-text tracking-tight">
                  QueryMind AI
                </h1>
              </div>

              <div className="flex items-center gap-3">
                {selectedDatabase && (
                  <div className="glass-effect px-4 py-2 rounded-lg flex items-center gap-2 border border-primary-500/20">
                    <Database className="w-4 h-4 text-primary-400" />
                    <span className="text-sm font-medium">{selectedDatabase.name}</span>
                  </div>
                )}

                <button
                  onClick={() => setShowSchema(!showSchema)}
                  className={`p-2 rounded-lg transition-all flex items-center gap-2 px-3 ${showSchema ? 'bg-primary-600 shadow-lg shadow-primary-600/30' : 'glass-effect hover:bg-white/10'
                    }`}
                  title="Toggle Schema Visualizer"
                >
                  <Settings className="w-5 h-5" />
                  <span className="text-sm font-medium hidden sm:inline">Visualizer</span>
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Main layout */}
        <div className="flex flex-1 overflow-hidden">
          {/* Sidebar */}
          <motion.aside
            initial={false}
            animate={{ width: sidebarOpen ? 320 : 0 }}
            className="glass-effect border-r border-white/10 overflow-hidden flex flex-col shrink-0"
          >
            <div className="p-5 flex flex-col h-full gap-6 overflow-y-auto" style={{ width: 320 }}>
              {/* Databases Section */}
              <section>
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest">
                    Databases
                  </h3>
                  <button
                    onClick={() => setIsAddDbOpen(true)}
                    className="p-1.5 hover:bg-primary-600/20 text-primary-400 rounded-md transition-colors"
                    title="Add Database"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                </div>

                <div className="space-y-2">
                  {databases?.map((db) => (
                    <button
                      key={db.id}
                      onClick={() => setSelectedDatabase(db)}
                      className={`w-full text-left p-3 rounded-xl transition-all border ${selectedDatabase?.id === db.id
                        ? 'bg-primary-600/20 border-primary-500/50'
                        : 'glass-effect border-transparent hover:border-white/10 hover:bg-white/5'
                        }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`p-2 rounded-lg ${selectedDatabase?.id === db.id ? 'bg-primary-500 text-white' : 'bg-white/5 text-gray-400'}`}>
                          <Database className="w-4 h-4" />
                        </div>
                        <div>
                          <div className={`text-sm font-semibold ${selectedDatabase?.id === db.id ? 'text-white' : 'text-gray-300'}`}>
                            {db.name}
                          </div>
                          <div className="text-[10px] text-gray-500 font-mono uppercase">
                            {db.db_type}
                          </div>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </section>

              {/* Tables Section */}
              {selectedDatabase && (
                <section>
                  <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3">
                    Tables
                  </h3>
                  <div className="space-y-1">
                    {schema?.tables && Object.keys(schema.tables).length > 0 ? (
                      Object.keys(schema.tables).map((tableName) => (
                        <button
                          key={tableName}
                          onClick={() => setSelectedTable(schema.tables[tableName])}
                          className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-all flex items-center justify-between group ${selectedTable?.name === tableName
                            ? 'bg-white/10 text-white'
                            : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
                            }`}
                        >
                          <div className="flex items-center gap-2">
                            <Table className="w-4 h-4 opacity-50" />
                            <span>{tableName}</span>
                          </div>
                          <ChevronRight className={`w-3 h-3 transition-transform ${selectedTable?.name === tableName ? 'rotate-90' : 'group-hover:translate-x-0.5'}`} />
                        </button>
                      ))
                    ) : (
                      <div className="text-xs text-gray-600 italic px-3">No tables found</div>
                    )}
                  </div>
                </section>
              )}

              {/* History Section */}
              <section className="mt-auto pt-6 border-t border-white/5">
                <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3 flex items-center gap-2">
                  <History className="w-3 h-3" />
                  Recent History
                </h3>
                <div className="space-y-2">
                  {queryHistory?.slice(0, 5).map((query) => (
                    <div
                      key={query.id}
                      className="p-3 glass-effect rounded-lg text-xs hover:bg-white/5 transition-all cursor-pointer border border-transparent hover:border-white/5"
                    >
                      <div className="text-gray-400 line-clamp-2 leading-relaxed">
                        {query.natural_language_query}
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            </div>
          </motion.aside>

          {/* Main content area */}
          <main className="flex-1 overflow-y-auto overflow-x-hidden relative">
            <div className="max-w-7xl mx-auto p-6 space-y-6 pb-32">
              {/* Schema Visualizer */}
              <AnimatePresence>
                {showSchema && schema && (
                  <motion.div
                    initial={{ opacity: 0, height: 0, y: -20 }}
                    animate={{ opacity: 1, height: 600, y: 0 }}
                    exit={{ opacity: 0, height: 0, y: -20 }}
                    className="card h-[600px] relative overflow-hidden group shadow-2xl shadow-primary-900/10"
                  >
                    <div className="absolute inset-0 bg-gradient-to-b from-primary-500/5 to-transparent pointer-events-none" />
                    <SchemaVisualizer3D
                      schema={schema}
                      onTableSelect={setSelectedTable}
                      selectedTable={selectedTable}
                    />
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Selected Table Detail View */}
              <AnimatePresence>
                {selectedTable && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 20 }}
                    className="card border-l-4 border-l-primary-500"
                  >
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-primary-500/10 rounded-lg text-primary-400">
                          <Table className="w-5 h-5" />
                        </div>
                        <h3 className="text-lg font-bold text-white">{selectedTable.name}</h3>
                      </div>
                      <button
                        onClick={() => setSelectedTable(null)}
                        className="text-gray-500 hover:text-white transition-colors"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                      {selectedTable.columns.map((col) => (
                        <div key={col.name} className="glass-effect p-4 rounded-xl border border-white/5 hover:border-primary-500/30 transition-all">
                          <div className="text-sm font-bold text-gray-200 mb-1 flex items-center gap-2">
                            {col.name}
                            {col.primary_key && <span className="text-[10px] bg-primary-500/20 text-primary-400 px-1.5 py-0.5 rounded uppercase font-mono">PK</span>}
                          </div>
                          <div className="text-xs text-gray-500 font-mono uppercase">{col.type}</div>
                        </div>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Query Area */}
              <div className="max-w-4xl mx-auto space-y-6">
                <QueryInput
                  onSubmit={handleQuerySubmit}
                  isLoading={executeMutation.isPending}
                />

                {latestQuery && (
                  <ResultsDisplay query={latestQuery} />
                )}

                {!latestQuery && !executeMutation.isPending && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="card text-center py-20 bg-gradient-to-b from-white/[0.02] to-transparent border-white/5"
                  >
                    <div className="max-w-lg mx-auto">
                      <div className="w-20 h-20 bg-primary-500/10 rounded-full flex items-center justify-center mx-auto mb-6 text-primary-400">
                        <Search className="w-10 h-10" />
                      </div>
                      <h2 className="text-3xl font-bold text-white mb-4">
                        Ready for Insights?
                      </h2>
                      <p className="text-gray-400 mb-10 leading-relaxed text-lg">
                        Connect your data and ask anything. Our AI will handle the
                        complex SQL, so you can focus on the answers.
                      </p>
                      <div className="grid grid-cols-1 gap-4">
                        {[
                          'Show me sales trends for the last quarter',
                          'Which customers have the highest lifetime value?',
                          'What are the most popular products this month?',
                        ].map((example, index) => (
                          <button
                            key={index}
                            onClick={() => handleQuerySubmit(example)}
                            className="group p-5 glass-effect rounded-2xl border border-white/5 hover:border-primary-500/50 hover:bg-primary-500/5 transition-all text-left flex items-center justify-between"
                          >
                            <span className="text-gray-300 group-hover:text-white transition-colors capitalize px-2">
                              "{example}"
                            </span>
                            <div className="w-8 h-8 rounded-full bg-white/5 group-hover:bg-primary-500 text-gray-500 group-hover:text-white flex items-center justify-center transition-all opacity-0 group-hover:opacity-100">
                              <Plus className="w-4 h-4" />
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}
              </div>
            </div>
          </main>
        </div>

        {/* Add Database Modal */}
        <AnimatePresence>
          {isAddDbOpen && (
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setIsAddDbOpen(false)}
                className="absolute inset-0 bg-black/80 backdrop-blur-sm"
              />
              <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 20 }}
                className="relative w-full max-w-lg glass-effect border border-white/10 rounded-2xl shadow-2xl overflow-hidden p-8"
              >
                <div className="flex items-center justify-between mb-8">
                  <div className="flex items-center gap-3">
                    <div className="p-3 bg-primary-500/10 rounded-xl text-primary-400">
                      <Plus className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Add New Database</h3>
                      <p className="text-sm text-gray-500">Connect a new data source to start querying</p>
                    </div>
                  </div>
                  <button
                    onClick={() => setIsAddDbOpen(false)}
                    className="p-2 hover:bg-white/5 rounded-lg text-gray-500 hover:text-white transition-all"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                <form onSubmit={handleAddDb} className="space-y-6">
                  <div className="space-y-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-gray-500 uppercase tracking-wider px-1">Connection Name</label>
                      <input
                        type="text"
                        placeholder="e.g. Production PostgreSQL"
                        value={newDb.name}
                        onChange={(e) => setNewDb({ ...newDb, name: e.target.value })}
                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition-all placeholder:text-gray-600"
                        required
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-1.5">
                        <label className="text-xs font-bold text-gray-500 uppercase tracking-wider px-1">System Type</label>
                        <select
                          value={newDb.db_type}
                          onChange={(e) => setNewDb({ ...newDb, db_type: e.target.value as any })}
                          className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary-500 transition-all appearance-none cursor-pointer"
                        >
                          <option value="postgresql" className="bg-[#1a1a1f]">PostgreSQL</option>
                          <option value="mysql" className="bg-[#1a1a1f]">MySQL</option>
                          <option value="mongodb" className="bg-[#1a1a1f]">MongoDB</option>
                          <option value="sqlite" className="bg-[#1a1a1f]">SQLite</option>
                        </select>
                      </div>
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-gray-500 uppercase tracking-wider px-1">Connection URI</label>
                      <div className="relative">
                        <input
                          type="password"
                          placeholder="postgresql://user:pass@host:port/db"
                          value={newDb.connection_string}
                          onChange={(e) => setNewDb({ ...newDb, connection_string: e.target.value })}
                          className="w-full bg-white/5 border border-white/10 rounded-xl pl-4 pr-12 py-3 text-white focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition-all placeholder:text-gray-600"
                          required
                        />
                        <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-600">
                          <Shield className="w-5 h-5" />
                        </div>
                      </div>
                      <p className="text-[10px] text-gray-600 px-1 mt-1 font-medium">Your credentials are encrypted and stored securely.</p>
                    </div>
                  </div>

                  <div className="flex gap-3 pt-4">
                    <button
                      type="button"
                      onClick={() => setIsAddDbOpen(false)}
                      className="flex-1 py-4 bg-white/5 hover:bg-white/10 text-white font-bold rounded-xl transition-all border border-white/5"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={addDbMutation.isPending}
                      className="flex-[2] py-4 bg-primary-600 hover:bg-primary-500 disabled:opacity-50 text-white font-bold rounded-xl transition-all shadow-xl shadow-primary-600/20 active:scale-[0.98]"
                    >
                      {addDbMutation.isPending ? 'Connecting...' : 'Test & Save Connection'}
                    </button>
                  </div>
                </form>
              </motion.div>
            </div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
