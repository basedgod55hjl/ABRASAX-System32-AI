/**
 * ═══════════════════════════════════════════════════════════════════
 * ABRASAX SmartScreen TOOLS — wires smartscreen.dll into agent tools
 * PRIMAL_HEX: 4f5349524953424c58434b | φ = 1.618033988749895
 * Bridges to smartscreen_wire.py for ctypes access to all 17 exports
 * ═══════════════════════════════════════════════════════════════════
 */
import { execSync } from 'child_process';
import { type ToolDefinition, type ToolResult, registerTool } from './abrasax_tools.js';

const SS_WIRE = 'python "C:\\Users\\BASEDGOD\\Desktop\\ABRASAX\\smartscreen_wire.py"';

// ── SmartScreen TOOL DEFINITIONS ──
export const SMARTScreen_TOOLS: ToolDefinition[] = [
  {
    type: 'function',
    function: {
      name: 'ss_check_file',
      description: 'Check any file reputation using Microsoft SmartScreen ML (Anaheim engine). Uses bloom filter + token-weighted model scoring. Returns score and verdict.',
      parameters: {
        type: 'object',
        properties: {
          path: { type: 'string', description: 'Absolute path to file to check' }
        },
        required: ['path'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'ss_check_url',
      description: 'Check URL reputation via SmartScreen UriReputationFactory. Uses the token-based ML model (uri_reputation.cpp) for scoring.',
      parameters: {
        type: 'object',
        properties: {
          url: { type: 'string', description: 'URL to check' }
        },
        required: ['url'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'ss_enforcement',
      description: 'Get or set SmartScreen enforcement levels (0=OFF, 1=WARN, 2=BLOCK). Can read all 3 policies: general, app_reputation, app_control.',
      parameters: {
        type: 'object',
        properties: {
          action: { type: 'string', enum: ['get', 'set'], description: 'Get current levels or set new levels', default: 'get' },
          level: { type: 'integer', description: 'Enforcement level: 0=OFF, 1=WARN, 2=BLOCK (required for set)' },
        },
        required: [],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'ss_clear_cache',
      description: 'Clear SmartScreen local cache. Forces fresh model evaluation on next check.',
      parameters: {
        type: 'object',
        properties: {},
        required: [],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'ss_ml_info',
      description: 'Get SmartScreen ML architecture metadata: pipeline stages, bloom filters, token features, threat classes, model metrics. Full Anaheim-SmartScreen dissection.',
      parameters: {
        type: 'object',
        properties: {},
        required: [],
      },
    },
  },
];

// ── SmartScreen TOOL EXECUTORS ──

function runSSWire(cmd: string, arg: string): string {
  try {
    return execSync(`${SS_WIRE} ${cmd} "${arg}"`, {
      encoding: 'utf-8',
      timeout: 15000,
      windowsHide: true,
    }).trim();
  } catch (err: any) {
    const out = (err.stdout || '') + (err.stderr || '');
    return out || `{"error": "${err.message}"}`;
  }
}

registerTool('ss_check_file', async (args: any): Promise<ToolResult> => {
  try {
    const output = runSSWire('check-file', args.path);
    return { success: true, output };
  } catch (err: any) {
    return { success: false, output: '', error: err.message };
  }
});

registerTool('ss_check_url', async (args: any): Promise<ToolResult> => {
  try {
    const output = runSSWire('check-url', args.url);
    return { success: true, output };
  } catch (err: any) {
    return { success: false, output: '', error: err.message };
  }
});

registerTool('ss_enforcement', async (args: any): Promise<ToolResult> => {
  try {
    if (args.action === 'set' && args.level !== undefined) {
      const output = runSSWire('set-enforcement', String(args.level));
      return { success: true, output };
    } else {
      const output = runSSWire('enforcement', '');
      return { success: true, output };
    }
  } catch (err: any) {
    return { success: false, output: '', error: err.message };
  }
});

registerTool('ss_clear_cache', async (_args: any): Promise<ToolResult> => {
  try {
    const output = runSSWire('clear-cache', '');
    return { success: true, output };
  } catch (err: any) {
    return { success: false, output: '', error: err.message };
  }
});

registerTool('ss_ml_info', async (_args: any): Promise<ToolResult> => {
  try {
    const output = runSSWire('ml-info', '');
    return { success: true, output };
  } catch (err: any) {
    return { success: false, output: '', error: err.message };
  }
});
