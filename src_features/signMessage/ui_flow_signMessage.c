#include "shared_context.h"

UX_FLOW_DEF_NOCB(
    ux_sign_flow_1_step,
    pnn,
    {
      &C_icon_certificate,
      "Sign",
      "message",
    });
UX_FLOW_DEF_NOCB(
    ux_sign_flow_2_step,
    bnnn_paging,
    {
      .title = "Message hash",
      .text = strings.common.fullAddress,
    });
UX_FLOW_DEF_VALID(
    ux_sign_flow_3_step,
    pbb,
    io_seproxyhal_touch_signMessage_ok(NULL),
    {
      &C_icon_validate_14,
      "Sign",
      "message",
    });
UX_FLOW_DEF_VALID(
    ux_sign_flow_4_step,
    pbb,
    io_seproxyhal_touch_signMessage_cancel(NULL),
    {
      &C_icon_crossmark,
      "Cancel",
      "signature",
    });

const ux_flow_step_t *        const ux_sign_flow [] = {
  &ux_sign_flow_1_step,
  &ux_sign_flow_2_step,
  &ux_sign_flow_3_step,
  &ux_sign_flow_4_step,
  FLOW_END_STEP,
};

