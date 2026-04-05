const crypto = require('crypto');
const fs = require('fs');

console.log("======================================================");
console.log("Vision X ECU - Secure Update Gateway");
console.log("======================================================\n");

// ---------------------------------------------------------
// Step 1: Secure Handshake 
// Tool: HTTPS (TLS) + X.509 Certificates
// ---------------------------------------------------------
class ServerCertificate {
    static isValid() {
        console.log("[TLS] Verifying Server X.509 Certificate against Root CA...");
        // Emulating certificate verification
        return true;
    }
}

let Antigravity_Update_Package = null;

if (ServerCertificate.isValid()) {
    console.log("[TLS] Handshake valid. Establishing secure connection...\n");
    // Emulating the downloaded package containing the file
    Antigravity_Update_Package = {
        name: "Antigravity_Propulsion_Control_v1.0.bin",
        // Same byte representation as the mock in Python: b"\x00\x01\x02AntigravityEngine_Logic\xFF\xEE\xDD\xCC"
        file: Buffer.concat([
            Buffer.from([0x00, 0x01, 0x02]),
            Buffer.from("AntigravityEngine_Logic", 'utf-8'),
            Buffer.from([0xFF, 0xEE, 0xDD, 0xCC])
        ]),
        ai_flag: "SECURE" // Emulated AI Pre-Verification flag passed from OEM infrastructure
    };
    console.log(`[Network] Received Update Package: ${Antigravity_Update_Package.name}`);
} else {
    console.error("[TLS] Handshake failed! Aborting connection.");
    process.exit(1);
}


// ---------------------------------------------------------
// Step 2: Blockchain Cross-Verification
// Tool: Web3.js / Ethers.js
// ---------------------------------------------------------
class SmartContractMock {
    static getLatestHash(version) {
        console.log(`\n[Web3] Querying Smart Contract ledger for authoritative hash for version ${version}...`);
        try {
            // Mocking pulling data from the ledger we generated earlier
            const ledgerData = fs.readFileSync('oem_ledger.json', 'utf8');
            const ledger = JSON.parse(ledgerData);

            // Find the record for the current version
            const record = ledger.find(entry => entry.version === version);

            if (record) {
                console.log(`[Web3] Block located. Trusted Hash: ${record.hash}`);
                return record.hash;
            } else {
                throw new Error("Version record not found on blockchain.");
            }
        } catch (error) {
            console.error(`[Web3] Error querying blockchain: ${error.message}`);
            return null;
        }
    }
}

const targetVersion = "1.0";
const officialHash = SmartContractMock.getLatestHash(targetVersion);


// ---------------------------------------------------------
// Step 3: Local Integrity Check
// Tool: SHA-256
// ---------------------------------------------------------
class SHA256 {
    static calculate(buffer) {
        console.log("\n[Integrity] Calculating local SHA-256 hash of downloaded payload...");
        const hashResult = crypto.createHash('sha256').update(buffer).digest('hex');
        console.log(`[Integrity] Local Hash computed: ${hashResult}`);
        return hashResult;
    }
}

const localHash = SHA256.calculate(Antigravity_Update_Package.file);


// ---------------------------------------------------------
// Step 4: Multi-Factor Approval
// ---------------------------------------------------------
console.log("\n[Approval] Verifying Multi-Factor Authentication Requirements...");

function Execute_Install() {
    console.log("--> Starting flashing sequence...");
    setTimeout(() => {
        console.log("--> Flashing complete.");
        console.log("\n======================================================");
        console.log("Antigravity Module Online. Flight systems enabled.");
        console.log("======================================================");
    }, 1000);
}

function Trigger_Alert_System() {
    console.log("--> [DASHBOARD ALERT] CRITICAL: Payload integrity compromised or AI rejected! Potential tampering detected.");
}

function Reject_Update() {
    console.log("--> Update safely discarded. System remains on previous stable version.");
    process.exit(1);
}

// Compare generated hash with authoritative blockchain hash, and check AI flag
if (localHash === officialHash && Antigravity_Update_Package.ai_flag === "SECURE") {
    console.log("[Approval] SHA-256 Signatures MATCH.");
    console.log("[Approval] AI Security Flag is SECURE.");
    console.log("[Approval] OVERALL STATUS: VERIFIED. Proceeding with installation.");
    Execute_Install();
} else {
    console.log("[Approval] Verification Mismatch!");
    console.log(`  Expected Hash:   ${officialHash}`);
    console.log(`  Actual Hash:     ${localHash}`);
    console.log(`  AI Flag Status:  ${Antigravity_Update_Package.ai_flag}`);
    Trigger_Alert_System();
    Reject_Update();
}