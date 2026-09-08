# Verifizierte Architektur-Befunde: HAI-TIKTOK @ 23d1346

Zusammengefuehrt aus 6 Karten mit Belegen: ling-3.0-flash-fin, mimo-v2.5, muse-spark-1.2, muse-spark-1.3, nemotron-3-ultra, nemotron-3.5-lightning.

Merge-Schluessel ist die Codestelle, nicht das Label. Jede Zeile unten wurde
gegen den committeten HEAD `23d1346fe3bb0040add32250b5939f56e46932e0` geprueft.

**54 belegte Konzepte.** `gefunden_von` = wie viele der 6 Karten mit Belegen diese Stelle nannten.

> Haeufigkeit ist kein Wichtigkeitsmass. Ein Konzept, das nur eine Karte fand,
> kann der zentrale Befund sein — solange es belegt ist.

## prisma/schema.prisma:1
- gefunden_von: 5/6 (ling-3.0-flash-fin, mimo-v2.5, muse-spark-1.2, muse-spark-1.3, nemotron-3-ultra)
- vergebene Labels: SQLite | SQLite (Posts) | SQLite (Prisma) | SQLite / Prisma
```
// This is your Prisma schema file,
// learn more about it in the docs: https://pris.ly/d/prisma-schema

```

## scripts/hai_tiktok_worker.py:1
- gefunden_von: 5/6 (ling-3.0-flash-fin, mimo-v2.5, muse-spark-1.3, nemotron-3-ultra, nemotron-3.5-lightning)
- vergebene Labels: File Queue | Hermes API | Hermes CLI | NotebookLM CLI | NotebookLM Pipeline | Pipeline Scripts | Video-Worker | Worker Process
```
#!/usr/bin/env python3
"""HAI TikTok worker: one queued session -> one NotebookLM video."""
from __future__ import annotations
```

## src/app/api/v1/posts/route.ts:80
- gefunden_von: 4/6 (mimo-v2.5, muse-spark-1.2, muse-spark-1.3, nemotron-3-ultra)
- vergebene Labels: HAI API | HAI Agenten | Next.js API Routes | Posts-API
```
export async function POST(req: NextRequest) {
  if (!(await requireApiAuth(req))) return unauthorized();

```

## src/app/page.tsx:1
- gefunden_von: 4/6 (ling-3.0-flash-fin, muse-spark-1.2, nemotron-3-ultra, nemotron-3.5-lightning)
- vergebene Labels: Next.js Web App | Page Components | User | Web Feed | Web Interface
```
import Link from "next/link";
import Feed from "@/components/Feed";
import { getPosts } from "@/lib/posts";
```

## src/lib/media.ts:1
- gefunden_von: 4/6 (ling-3.0-flash-fin, mimo-v2.5, nemotron-3-ultra, nemotron-3.5-lightning)
- vergebene Labels: Media Service | Media Storage
```
import "server-only";

import { randomUUID } from "node:crypto";
```

## scripts/hai_tiktok_pipeline.py:1
- gefunden_von: 3/6 (ling-3.0-flash-fin, mimo-v2.5, nemotron-3.5-lightning)
- vergebene Labels: NotebookLM Pipeline | Pipeline Coordinator | Pipeline Scripts
```
"""Durable coordinator for one script producer and one NotebookLM consumer.

Executor tasks return values. Only this coordinator mutates job/queue ledgers.
```

## scripts/hai_tiktok_pipeline.py:73
- gefunden_von: 3/6 (muse-spark-1.2, muse-spark-1.3, nemotron-3-ultra)
- vergebene Labels: Pipeline Coordinator | Pipeline-Koordinator | Worker Pipeline
```
class Coordinator:
    def __init__(self, worker, *, producer_executor=None, consumer_executor=None,
                 clock=time.time, poll_seconds=60):
```

## scripts/hai_tiktok_worker.py:735
- gefunden_von: 3/6 (ling-3.0-flash-fin, muse-spark-1.2, nemotron-3-ultra)
- vergebene Labels: NotebookLM | NotebookLM CLI | edge-tts Fallback
```
def add_source(nb, md, title):
    out=run([NLM,'source','add',nb,'--file',str(md),'--title',title,'--wait','--wait-timeout','600','--json'], 700)
    sid,_=parse_json_or_uuid(out)
```

## src/app/upload/page.tsx:1
- gefunden_von: 3/6 (ling-3.0-flash-fin, muse-spark-1.3, nemotron-3-ultra)
- vergebene Labels: Admin-UI | Next.js Web App | Page Components
```
"use client";

import { useEffect, useState } from "react";
```

## src/lib/auth.ts:119
- gefunden_von: 3/6 (muse-spark-1.2, muse-spark-1.3, nemotron-3-ultra)
- vergebene Labels: Auth Gate | Auth System | Auth-Gate
```
export async function requireApiAuth(req: Request): Promise<boolean> {
  if (verifyBearerToken(extractBearerToken(req))) return true;
  return requireAdminSession();
```

## src/lib/db.ts:30
- gefunden_von: 3/6 (mimo-v2.5, muse-spark-1.3, nemotron-3-ultra)
- vergebene Labels: SQLite | SQLite (Posts) | SQLite (Prisma)
```
function createPrismaClient(): PrismaClient {
  const adapter = new PrismaBetterSqlite3({
    url: resolveSqliteUrl(process.env.DATABASE_URL),
```

## src/lib/media.ts:63
- gefunden_von: 3/6 (muse-spark-1.2, muse-spark-1.3, nemotron-3-ultra)
- vergebene Labels: Media Storage | Media Store | Media-Store
```
export async function saveUpload(
  file: File,
  mime: string
```

## src/middleware.ts:1
- gefunden_von: 3/6 (ling-3.0-flash-fin, mimo-v2.5, muse-spark-1.3)
- vergebene Labels: Auth Middleware | Auth-Gate | Middleware
```
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

```

## docker-entrypoint.sh:1
- gefunden_von: 2/6 (ling-3.0-flash-fin, mimo-v2.5)
- vergebene Labels: Docker | Docker Runtime
```
#!/bin/sh
# Runs on every container start before the Next.js server boots.
#  1. Makes sure the bind-mounted data dirs exist (host volumes can start empty)
```

## scripts/hai-post.sh:1
- gefunden_von: 2/6 (mimo-v2.5, muse-spark-1.3)
- vergebene Labels: Agenten & Hooks | HAI Agenten
```
#!/usr/bin/env bash
# Agent helper for the HAI Agent-API (/api/v1/posts).
# Requires HAI_API_KEY; optional BASE_URL (default http://localhost:3000).
```

## scripts/hai_tiktok_worker.py:346
- gefunden_von: 2/6 (muse-spark-1.2, nemotron-3-ultra)
- vergebene Labels: Agent Sessions | Worker Pipeline
```
# One table instead of an if/else per call site: a new harness is added here
# once, and no caller can silently fall through to the wrong loader.
# Mapped by NAME, not by function object: holding the object would freeze the
```

## src/app/api/v1/ingest/notebooklm/route.ts:31
- gefunden_von: 2/6 (muse-spark-1.3, nemotron-3-ultra)
- vergebene Labels: Next.js API Routes | NotebookLM-Ingest
```
export async function POST(req: NextRequest) {
  if (!(await requireApiAuth(req))) return unauthorized();

```

## src/app/api/v1/posts/route.ts:1
- gefunden_von: 2/6 (ling-3.0-flash-fin, nemotron-3.5-lightning)
- vergebene Labels: API Routes
```
import { NextRequest, NextResponse } from "next/server";
import { requireApiAuth } from "@/lib/auth";
import { prisma } from "@/lib/db";
```

## src/app/api/v1/posts/route.ts:62
- gefunden_von: 2/6 (muse-spark-1.3, nemotron-3-ultra)
- vergebene Labels: Next.js API Routes | Posts-API
```
export async function GET(req: NextRequest) {
  if (!(await requireApiAuth(req))) return unauthorized();

```

## src/app/ingest/page.tsx:1
- gefunden_von: 2/6 (ling-3.0-flash-fin, nemotron-3-ultra)
- vergebene Labels: Next.js Web App | Page Components
```
"use client";

import { useEffect, useState } from "react";
```

## src/app/page.tsx:24
- gefunden_von: 2/6 (mimo-v2.5, muse-spark-1.3)
- vergebene Labels: Browser / Handy | Feed-Web
```
export default async function Home() {
  const posts = await getPosts();

```

## src/lib/auth.ts:1
- gefunden_von: 2/6 (ling-3.0-flash-fin, nemotron-3.5-lightning)
- vergebene Labels: Auth API | Auth Library
```
import crypto from "node:crypto";
import { cookies } from "next/headers";

```

## src/lib/db.ts:1
- gefunden_von: 2/6 (ling-3.0-flash-fin, nemotron-3.5-lightning)
- vergebene Labels: Prisma / SQLite | SQLite / Prisma
```
import "server-only";

import path from "node:path";
```

## src/lib/media.ts:84
- gefunden_von: 2/6 (mimo-v2.5, nemotron-3-ultra)
- vergebene Labels: Media Storage
```
export function resolveMediaPath(relativePath: string): string | null {
  const mediaDir = path.resolve(getMediaDir());
  const absolutePath = path.resolve(mediaDir, relativePath);
```

## Dockerfile:1
- gefunden_von: 1/6 (ling-3.0-flash-fin)
- vergebene Labels: Docker Runtime
```
# syntax=docker/dockerfile:1

# HAI-TIKTOK — multi-stage Docker build
```

## docker-compose.yml:1
- gefunden_von: 1/6 (mimo-v2.5)
- vergebene Labels: Docker
```
services:
  app:
    build:
```

## mobile/src/lib/api.ts:30
- gefunden_von: 1/6 (muse-spark-1.3)
- vergebene Labels: Expo-App
```
export async function mediaUrl(mediaPath: string): Promise<string> {
  const base = await getBaseUrl();
  const clean = mediaPath.replace(/^\/+/, '');
```

## mobile/src/lib/api.ts:79
- gefunden_von: 1/6 (muse-spark-1.3)
- vergebene Labels: Expo-App
```
export async function fetchPosts(): Promise<Post[]> {
  const response = await request('/api/v1/posts');
  if (!response.ok) {
```

## mobile/src/screens/FeedScreen.tsx:27
- gefunden_von: 1/6 (muse-spark-1.2)
- vergebene Labels: Mobile App
```
export function FeedScreen({ onOpenSettings, onOpenCompose }: FeedScreenProps) {
  const insets = useSafeAreaInsets();
  const [posts, setPosts] = useState<Post[]>([]);
```

## next.config.ts:3
- gefunden_von: 1/6 (mimo-v2.5)
- vergebene Labels: Next.js App
```
const nextConfig: NextConfig = {
  output: "standalone",
  serverExternalPackages: ["@prisma/client", "@prisma/adapter-better-sqlite3", "better-sqlite3"],
```

## package.json:1
- gefunden_von: 1/6 (ling-3.0-flash-fin)
- vergebene Labels: Next.js App
```
{
  "name": "hai-tiktok",
  "version": "0.1.0",
```

## scripts/hai-from-notebooklm.sh:77
- gefunden_von: 1/6 (muse-spark-1.3)
- vergebene Labels: Agenten & Hooks
```
  "${BASE_URL%/}/api/v1/ingest/notebooklm"
echo
```

## scripts/hai_tiktok_pipeline.py:563
- gefunden_von: 1/6 (muse-spark-1.3)
- vergebene Labels: Pipeline-Koordinator
```
def run(worker, *, max_seconds=0, poll_seconds=60, once=False, consume_only=False):
    coordinator = Coordinator(worker, poll_seconds=poll_seconds)
    started = time.monotonic()
```

## scripts/hai_tiktok_script_optimizer.py:148
- gefunden_von: 1/6 (muse-spark-1.2)
- vergebene Labels: Script Optimizer
```
def assess(source, script, chat):
    prompt = f"""{RULES}\n{RUBRIC}
Antworte nur mit JSON:
```

## scripts/hai_tiktok_worker.py:51
- gefunden_von: 1/6 (nemotron-3-ultra)
- vergebene Labels: Telegram
```
def send_telegram(text, timeout=60):
    if not NOTIFY:
        return
```

## scripts/hai_tiktok_worker.py:89
- gefunden_von: 1/6 (muse-spark-1.3)
- vergebene Labels: Video-Worker
```
def parse_queue_line(line):
    parts=line.split('\t')
    if len(parts) < 2 or not parts[0].strip() or not parts[1].strip():
```

## scripts/hai_tiktok_worker.py:215
- gefunden_von: 1/6 (nemotron-3.5-lightning)
- vergebene Labels: NotebookLM
```
    if payload.get('originator') != 'codex-tui': return False
    return isinstance(payload.get('source'), str)

```

## scripts/hai_tiktok_worker.py:254
- gefunden_von: 1/6 (nemotron-3-ultra)
- vergebene Labels: Worker Pipeline
```
def pick_oldest():
    # Keep the provider lane serial: finish/download one requested video before
    # ordering the next. This avoids turning a session burst into a quota burst.
```

## scripts/hai_tiktok_worker.py:427
- gefunden_von: 1/6 (nemotron-3-ultra)
- vergebene Labels: Hermes CLI
```
    """Independent text-only calls; mark internal sessions to avoid self-ingest."""
    provider, model = DISTILL_MODEL
    return run([HERMES, 'chat', '--query-file', '-', '--provider', provider,
```

## scripts/hai_tiktok_worker.py:764
- gefunden_von: 1/6 (nemotron-3-ultra)
- vergebene Labels: edge-tts Fallback
```
def build_fallback_video(script_text, mp4_path):
    """Free, unlimited local fallback when NotebookLM quota is hit:
    edge-tts (already used elsewhere in this system) for narration +
```

## scripts/hai_tiktok_worker.py:871
- gefunden_von: 1/6 (nemotron-3-ultra)
- vergebene Labels: Telegram
```
    send_telegram(f"{entry.get('title','HAI TikTok')}\nMEDIA:{vertical}", 120)
    play_sound('complete.oga')
    print('NOTEBOOKLM_FETCHED', vertical)
```

## scripts/hai_tiktok_worker.py:984
- gefunden_von: 1/6 (muse-spark-1.2)
- vergebene Labels: Session Worker
```
def process_one():
    try: reap_inflight()
    except Exception as e: print(f'REAP_FAILED: {e}', file=sys.stderr)
```

## src/app/api/media/[...path]/route.ts:1
- gefunden_von: 1/6 (ling-3.0-flash-fin)
- vergebene Labels: API Routes
```
import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { Readable } from "node:stream";
```

## src/app/api/media/[...path]/route.ts:62
- gefunden_von: 1/6 (muse-spark-1.3)
- vergebene Labels: Media-Store
```
export async function GET(req: NextRequest, context: RouteContext) {
  const { path: segments } = await context.params;
  const relativePath = segments.map(decodeURIComponent).join("/");
```

## src/app/api/v1/ingest/notebooklm/route.ts:1
- gefunden_von: 1/6 (ling-3.0-flash-fin)
- vergebene Labels: API Routes
```
import { NextRequest, NextResponse } from "next/server";
import { requireApiAuth } from "@/lib/auth";
import { prisma } from "@/lib/db";
```

## src/app/layout.tsx:1
- gefunden_von: 1/6 (ling-3.0-flash-fin)
- vergebene Labels: Next.js App
```
import type { Metadata, Viewport } from "next";
import { Syne, Manrope } from "next/font/google";
import "./globals.css";
```

## src/app/layout.tsx:35
- gefunden_von: 1/6 (mimo-v2.5)
- vergebene Labels: Next.js App
```
export default function RootLayout({
  children,
}: Readonly<{
```

## src/components/Feed.tsx:53
- gefunden_von: 1/6 (mimo-v2.5)
- vergebene Labels: Browser / Handy
```
export default function Feed({ posts }: { posts: Post[] }) {
  const router = useRouter();
  const scrollRef = useRef<HTMLDivElement>(null);
```

## src/components/Feed.tsx:192
- gefunden_von: 1/6 (mimo-v2.5)
- vergebene Labels: Feed UI
```
      <div ref={scrollRef} className="feed-scroll">
        {posts.map((post) => (
          <FeedItem key={post.id} post={post} />
```

## src/components/FeedItem.tsx:1
- gefunden_von: 1/6 (mimo-v2.5)
- vergebene Labels: Feed UI
```
import type { Post, PostSource } from "@/lib/types";
import { mediaUrl, toCreatedAt } from "@/lib/types";
import VideoSlide from "./VideoSlide";
```

## src/components/NotebookIngestForm.tsx:35
- gefunden_von: 1/6 (muse-spark-1.3)
- vergebene Labels: Admin-UI
```
      const res = await fetch("/api/v1/ingest/notebooklm", {
        method: "POST",
        credentials: "include",
```

## src/lib/auth.ts:70
- gefunden_von: 1/6 (nemotron-3-ultra)
- vergebene Labels: Auth System
```
export function verifyAdminPassword(password: unknown): boolean {
  if (typeof password !== "string" || password.length === 0) return false;
  return timingSafeEqualStrings(password, getAdminPassword());
```

## src/lib/notebooklm.ts:5
- gefunden_von: 1/6 (muse-spark-1.3)
- vergebene Labels: NotebookLM-Ingest
```
export function splitNotebookContent(
  markdown: string,
  maxChars = 480
```

## src/lib/posts.ts:21
- gefunden_von: 1/6 (muse-spark-1.3)
- vergebene Labels: Feed-Web
```
export async function getPosts(): Promise<Post[]> {
  try {
    const rows = await prisma.post.findMany({
```

## Nicht verifizierbar (nicht verwenden)

- `.codex/sessions/:1` — behauptet von nemotron-3.5-lightning, Stelle im HEAD leer oder nicht vorhanden
