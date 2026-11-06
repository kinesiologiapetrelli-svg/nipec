<?php
/**
 * Riceve il modulo dei contatti di nipecestetica.eu.
 *
 * Fa tre cose, in quest'ordine, e nessuna delle tre puo' far fallire
 * le altre:
 *   1. salva la richiesta in dati/richieste.csv
 *   2. manda una email a info@nipecestetica.com
 *   3. risponde al browser, che poi apre WhatsApp
 *
 * Senza JavaScript il modulo funziona lo stesso: arriva qui con un
 * POST normale e riceve una pagina di conferma.
 */

declare(strict_types=1);

const DESTINATARIO = 'info@nipecestetica.com';
const MITTENTE     = 'sito@nipecestetica.eu';
const CARTELLA     = __DIR__ . '/dati';
const CSV          = CARTELLA . '/richieste.csv';
const MAX_CAMPO    = 2000;
const ATTESA_MIN   = 3;      // secondi: sotto questa soglia e' un robot
const MAX_PER_ORA  = 12;     // richieste per indirizzo IP

/* ------------------------------------------------------------------ */

function pulisci(string $v): string {
    $v = str_replace(["\r\n", "\r"], "\n", $v);
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v) ?? '';
    return mb_substr(trim($v), 0, MAX_CAMPO);
}

/**
 * Impedisce che un valore come "=cmd()" diventi una formula in Excel.
 * Un numero di telefono come "+39 333..." non e' una formula: dopo il
 * segno c'e' una cifra, quindi si lascia com'e'.
 */
function sicuro_per_csv(string $v): string {
    if ($v === '') return $v;
    if (strpbrk($v[0], "=@\t\r") !== false) return "'" . $v;
    if (($v[0] === '+' || $v[0] === '-') && !preg_match('/^[+-][\d\s]/', $v)) {
        return "'" . $v;
    }
    return $v;
}

/** Niente a capo nei campi dell'intestazione: eviterebbe un'iniezione. */
function sicuro_per_intestazione(string $v): string {
    return trim(str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v));
}

function ip(): string {
    $v = $_SERVER['REMOTE_ADDR'] ?? '';
    return filter_var($v, FILTER_VALIDATE_IP) ? $v : '0.0.0.0';
}

function troppe_richieste(): bool {
    $f = CARTELLA . '/limite.json';
    $ora = time();
    $d = is_readable($f) ? (json_decode((string)file_get_contents($f), true) ?: []) : [];
    foreach ($d as $k => $lista) {
        $d[$k] = array_values(array_filter($lista, fn($t) => $ora - $t < 3600));
        if (!$d[$k]) unset($d[$k]);
    }
    $k = hash('sha256', ip());
    $d[$k] ??= [];
    if (count($d[$k]) >= MAX_PER_ORA) return true;
    $d[$k][] = $ora;
    @file_put_contents($f, json_encode($d), LOCK_EX);
    return false;
}

function prepara_cartella(): void {
    if (!is_dir(CARTELLA)) @mkdir(CARTELLA, 0750, true);
    // doppia cintura: il .htaccess nega l'accesso dal web
    $h = CARTELLA . '/.htaccess';
    if (!file_exists($h)) {
        @file_put_contents($h,
            "Require all denied\n<IfModule !mod_authz_core.c>\nDeny from all\n</IfModule>\n");
    }
}

function rispondi(bool $ok, string $messaggio): never {
    $ajax = isset($_POST['ajax'])
        || str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');
    if ($ajax) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'messaggio' => $messaggio], JSON_UNESCAPED_UNICODE);
        exit;
    }
    $t = htmlspecialchars($messaggio, ENT_QUOTES, 'UTF-8');
    header('Content-Type: text/html; charset=utf-8');
    echo '<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">'
       . '<meta name="viewport" content="width=device-width,initial-scale=1">'
       . '<meta name="robots" content="noindex"><title>NIPEC</title>'
       . '<style>body{font-family:system-ui,sans-serif;background:#123A63;color:#fff;'
       . 'display:grid;place-items:center;min-height:100vh;margin:0;padding:24px;'
       . 'text-align:center;line-height:1.6}a{color:#9CCBE8}</style></head><body><div>'
       . '<h1 style="font-size:1.5rem">' . $t . '</h1>'
       . '<p><a href="/">Torna al sito</a></p></div></body></html>';
    exit;
}

/* ------------------------------------------------------------------ */

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /contatti.html', true, 303);
    exit;
}

prepara_cartella();

// --- segnalazione di un clic su WhatsApp: si registra e basta -------
if (($_POST['evento'] ?? '') === 'whatsapp') {
    $riga = [date('c'), 'clic-whatsapp', pulisci((string)($_POST['pagina'] ?? '')),
             hash('sha256', ip() . date('Y-m-d'))];
    if ($fh = @fopen(CARTELLA . '/eventi.csv', 'a')) {
        @flock($fh, LOCK_EX); @fputcsv($fh, $riga); @fclose($fh);
    }
    http_response_code(204);
    exit;
}

// --- anti-robot -----------------------------------------------------
if (pulisci((string)($_POST['azienda_extra'] ?? '')) !== '') {   // campo trappola
    rispondi(true, 'Grazie, ti ricontattiamo presto.');          // bugia voluta
}
$aperta = (int)($_POST['t'] ?? 0);
if ($aperta > 0 && (time() - $aperta) < ATTESA_MIN) {
    rispondi(false, 'Richiesta inviata troppo in fretta. Riprova fra qualche secondo.');
}
if (troppe_richieste()) {
    rispondi(false, 'Hai gia\' inviato diverse richieste. Scrivici su WhatsApp.');
}

// --- i campi --------------------------------------------------------
$campi = [
    'nome'      => 'Nome e cognome',
    'telefono'  => 'Telefono / WhatsApp',
    'email'     => 'Email',
    'centro'    => 'Nome del centro',
    'citta'     => 'Citta',
    'interesse' => 'Cosa interessa',
    'messaggio' => 'Messaggio',
];
$v = [];
foreach ($campi as $k => $_) $v[$k] = pulisci((string)($_POST[$k] ?? ''));

if ($v['nome'] === '' || $v['telefono'] === '') {
    rispondi(false, 'Servono almeno il nome e un recapito telefonico.');
}
if (empty($_POST['privacy'])) {
    rispondi(false, 'Serve il consenso al trattamento dei dati.');
}
if ($v['email'] !== '' && !filter_var($v['email'], FILTER_VALIDATE_EMAIL)) {
    rispondi(false, 'L\'indirizzo email non sembra valido.');
}

// --- 1. salva -------------------------------------------------------
$nuovo = !file_exists(CSV);
if ($fh = @fopen(CSV, 'a')) {
    @flock($fh, LOCK_EX);
    if ($nuovo) {
        @fwrite($fh, "\xEF\xBB\xBF");            // BOM, cosi' Excel legge gli accenti
        @fputcsv($fh, ['Data', ...array_values($campi), 'Consenso privacy', 'Pagina', 'Lingua']);
    }
    @fputcsv($fh, array_map('sicuro_per_csv', [
        date('Y-m-d H:i:s'), ...array_values($v), 'si',
        pulisci((string)($_POST['pagina'] ?? '')),
        pulisci((string)($_POST['lingua'] ?? '')),
    ]));
    @fclose($fh);
}

// --- 2. avvisa via email -------------------------------------------
$righe = [];
foreach ($campi as $k => $etichetta) {
    if ($v[$k] !== '') $righe[] = $etichetta . ': ' . $v[$k];
}
$corpo = "Nuova richiesta dal sito nipecestetica.eu\n\n"
       . implode("\n", $righe)
       . "\n\nRicevuta il " . date('d/m/Y \a\l\l\e H:i')
       . "\nPagina: " . pulisci((string)($_POST['pagina'] ?? '-')) . "\n";

$intestazioni = [
    'From: NIPEC sito <' . MITTENTE . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: nipecestetica.eu',
];
if ($v['email'] !== '') {
    $intestazioni[] = 'Reply-To: ' . sicuro_per_intestazione($v['nome'])
                    . ' <' . sicuro_per_intestazione($v['email']) . '>';
}
$oggetto = 'Richiesta sito: ' . sicuro_per_intestazione($v['nome']);
if ($v['citta'] !== '') $oggetto .= ' (' . sicuro_per_intestazione($v['citta']) . ')';

@mail(DESTINATARIO, '=?UTF-8?B?' . base64_encode($oggetto) . '?=',
      $corpo, implode("\r\n", $intestazioni), '-f' . MITTENTE);

// --- 3. conferma ----------------------------------------------------
rispondi(true, 'Grazie, abbiamo ricevuto la tua richiesta. Ti ricontattiamo presto.');
