/*
 * LTE ML1 BPLMN Cell Confirm
 */

#include "consts.h"
#include "log_packet.h"
#include "log_packet_helper.h"

const Fmt LteMl1BplmnCellConfirm_Fmt [] = {
    {UINT, "Version", 1},
};

const Fmt LteMl1BplmnCellConfirm_Payload_v4 [] = {
    {UINT, "Standards Version", 1},
    {SKIP, NULL, 2},
    {UINT, "Frequency", 4},
    {UINT, "RSRP", 2}, // (x-65535)
    {SKIP, NULL, 2},
    {UINT, "BW", 1},
    {UINT, "Cell ID", 2},   // 10 bits
    {SKIP, NULL, 1},
    {UINT, "SRX Lev Calculated", 4}, // 1 bit
    {PLACEHOLDER, "SRX Lev", 0}, // 16 bits
};
const Fmt LteMl1BplmnCellConfirm_Rel9Info [] = {
    {UINT, "Rel 9 Info S Qual Calculated", 4},    // 1 bit
    {PLACEHOLDER, "Rel 9 Info S Qual", 0},  // 16 bits
};

const ValueName LteMl1BplmnCellConfirm_StandardsVersion [] = {
    {1, "Release 9"},
};
const ValueName LteMl1BplmnCellConfirm_SRXLevCalculated [] = {
    {0, "false"},
    {1, "true"},
};
const ValueName LteMl1BplmnCellConfirm_Rel9InfoSQualCalculated [] = {
    {0, "No"},
    {1, "Yes"},
};

static int _decode_lte_ml1_bplmn_cell_confirm_payload (const char *b,
        int offset, size_t length, PyObject *result) {
    int start = offset;
    int pkt_ver = _search_result_int(result, "Version");

    switch (pkt_ver) {
    case 4:
        {
            offset += _decode_by_fmt(LteMl1BplmnCellConfirm_Payload_v4,
                    ARRAY_SIZE(LteMl1BplmnCellConfirm_Payload_v4, Fmt),
                    b, offset, length, result);
            int iStandrdsVersion = _search_result_int(result,
                    "Standards Version");
            (void) _map_result_field_to_name(result,
                    "Standards Version",
                    LteMl1BplmnCellConfirm_StandardsVersion,
                    ARRAY_SIZE(LteMl1BplmnCellConfirm_StandardsVersion, ValueName),
                    "Unknown");
            int iRSRP = _search_result_int(result, "RSRP");
            iRSRP -= 65535;
            PyObject *old_object = _replace_result_int(result, "RSRP", iRSRP);
            Py_DECREF(old_object);
            unsigned int iNonDecodeP1 = _search_result_uint(result, "SRX Lev Calculated");
            int iSRXLevCalculated = iNonDecodeP1 & 1; // last 1 bits
            int iSRXLev = (iNonDecodeP1 >> 1) & 65535; // next 16 bits
            old_object = _replace_result_int(result, "SRX Lev Calculated",
                    iSRXLevCalculated);
            Py_DECREF(old_object);
            old_object = _replace_result_int(result, "SRX Lev",
                    iSRXLev);
            Py_DECREF(old_object);
            (void) _map_result_field_to_name(result,
                    "SRX Lev Calculated",
                    LteMl1BplmnCellConfirm_SRXLevCalculated,
                    ARRAY_SIZE(LteMl1BplmnCellConfirm_SRXLevCalculated, ValueName),
                    "Unknown");

            if (iStandrdsVersion == 1) {
                offset += _decode_by_fmt(LteMl1BplmnCellConfirm_Rel9Info,
                        ARRAY_SIZE(LteMl1BplmnCellConfirm_Rel9Info, Fmt),
                        b, offset, length, result);
                unsigned int iNonDecodeP2 = _search_result_uint(result,
                        "Rel 9 Info S Qual Calculated");
                int iR9SQCalculated = iNonDecodeP2 & 1; // last 1 bit
                int iR9SQual = (iNonDecodeP2 >> 1) & 65535; // next 16 bits
                old_object = _replace_result_int(result,
                        "Rel 9 Info S Qual Calculated", iR9SQCalculated);
                Py_DECREF(old_object);
                old_object = _replace_result_int(result,
                        "Rel 9 Info S Qual", iR9SQual);
                Py_DECREF(old_object);
                (void) _map_result_field_to_name(result,
                        "Rel 9 Info S Qual Calculated",
                        LteMl1BplmnCellConfirm_Rel9InfoSQualCalculated,
                        ARRAY_SIZE(LteMl1BplmnCellConfirm_Rel9InfoSQualCalculated,
                            ValueName),
                        "Unknown");
            }
            return offset - start;
        }
    default:
        printf("Unknown LTE PDSCH Stat Indication version: 0x%x\n", pkt_ver);
        return 0;
    }
}
