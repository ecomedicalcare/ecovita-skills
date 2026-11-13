#!/usr/bin/env node
// Copia desde ECC (github.com/affaan-m/ECC) las piezas listadas en skills.txt
// hacia plugins/ecovita/. Borra las que ya no estén en la lista.
//
// Uso:
//   node scripts/sincronizar.mjs                 # descarga la última versión de ECC
//   node scripts/sincronizar.mjs --origen <dir>  # usa una copia local de ECC
//
// Sin dependencias: solo Node 20+ y git.

import { execFileSync } from 'node:child_process';
import { cpSync, existsSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

const RAIZ = resolve(import.meta.dirname, '..');
const PLUGIN = join(RAIZ, 'plugins', 'ecovita');
const REPO_ECC = 'https://github.com/affaan-m/ECC.git';
const TIPOS = { skill: 'skills', agent: 'agents', command: 'commands' };

function leerLista() {
  const piezas = { skills: new Set(), agents: new Set(), commands: new Set() };
  const lineas = readFileSync(join(RAIZ, 'skills.txt'), 'utf8').split('\n');
  for (const [i, bruta] of lineas.entries()) {
    const linea = bruta.trim();
    if (!linea || linea.startsWith('#')) continue;
    const [tipo, nombre] = linea.split(':').map((p) => p?.trim());
    if (!TIPOS[tipo] || !/^[a-z0-9-]+$/.test(nombre ?? '')) {
      throw new Error(`skills.txt línea ${i + 1} no válida: "${linea}"`);
    }
    piezas[TIPOS[tipo]].add(nombre);
  }
  return piezas;
}

function obtenerEcc() {
  const i = process.argv.indexOf('--origen');
  if (i !== -1) return { dir: resolve(process.argv[i + 1]), temporal: false };
  const dir = mkdtempSync(join(tmpdir(), 'ecc-'));
  execFileSync('git', ['clone', '--depth', '1', '--quiet', REPO_ECC, dir], { stdio: 'inherit' });
  return { dir, temporal: true };
}

function ruta(base, carpeta, nombre) {
  return carpeta === 'skills' ? join(base, 'skills', nombre) : join(base, carpeta, `${nombre}.md`);
}

function nombreDe(carpeta, entrada) {
  return carpeta === 'skills' ? entrada : entrada.replace(/\.md$/, '');
}

function sincronizar() {
  const piezas = leerLista();
  const { dir: ecc, temporal } = obtenerEcc();
  const faltan = [];
  try {
    for (const [carpeta, nombres] of Object.entries(piezas)) {
      const destino = join(PLUGIN, carpeta);
      if (existsSync(destino)) {
        for (const entrada of readdirSync(destino)) {
          if (!nombres.has(nombreDe(carpeta, entrada))) rmSync(join(destino, entrada), { recursive: true });
        }
      }
      for (const nombre of nombres) {
        const origen = ruta(ecc, carpeta, nombre);
        if (!existsSync(origen)) { faltan.push(`${carpeta}/${nombre}`); continue; }
        const dest = ruta(PLUGIN, carpeta, nombre);
        rmSync(dest, { recursive: true, force: true });
        cpSync(origen, dest, { recursive: true });
      }
    }
    cpSync(join(ecc, 'LICENSE'), join(PLUGIN, 'LICENSE-ECC'));
    let commit = 'desconocido';
    try {
      commit = execFileSync('git', ['-C', ecc, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
    } catch { /* copia local sin git */ }
    const version = readFileSync(join(ecc, 'VERSION'), 'utf8').trim();
    writeFileSync(join(PLUGIN, 'ECC-VERSION'), `ECC ${version}\ncommit ${commit}\n`);
  } finally {
    if (temporal) rmSync(ecc, { recursive: true, force: true });
  }
  const total = Object.values(piezas).reduce((n, s) => n + s.size, 0);
  console.log(`Sincronizadas ${total - faltan.length} de ${total} piezas desde ECC.`);
  if (faltan.length) {
    console.error(`No existen en ECC (revisa skills.txt): ${faltan.join(', ')}`);
    process.exitCode = 1;
  }
}

sincronizar();
