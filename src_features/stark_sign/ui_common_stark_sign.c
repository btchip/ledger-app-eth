#ifdef HAVE_STARKWARE

#include "shared_context.h"
#include "stark_utils.h"

unsigned int io_seproxyhal_touch_stark_ok(const bagl_element_t *e) {
    uint8_t privateKeyData[32];
    uint8_t signatureLength;
    uint32_t tx = 0;
    io_seproxyhal_io_heartbeat();
    starkDerivePrivateKey(tmpCtx.transactionContext.bip32Path, tmpCtx.transactionContext.pathLength, privateKeyData);
    io_seproxyhal_io_heartbeat();
    tx = stark_sign(G_io_apdu_buffer, privateKeyData, dataContext.starkContext.w1, dataContext.starkContext.w2, dataContext.starkContext.w3);
    G_io_apdu_buffer[tx++] = 0x90;
    G_io_apdu_buffer[tx++] = 0x00;
    reset_app_context();
    // Send back the response, do not restart the event loop
    io_exchange(CHANNEL_APDU | IO_RETURN_AFTER_TX, tx);
    // Display back the original UX
    ui_idle();
    return 0; // do not redraw the widget
}

#endif
